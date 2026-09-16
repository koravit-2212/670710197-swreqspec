# แผนทางเทคนิค: จองคิวตรวจสุขภาพ (Booking)

## 1. สรุปแนวทาง (5 บรรทัด)
ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ เพื่อดูช่วงเวลาว่างและยืนยันการจองได้ในกระบวนการเดียว โดยใช้โมเดลการจองที่ป้องกันคิวซ้ำและลดจำนวนที่นั่งเมื่อยืนยันสำเร็จ ระบบจะต้องป้องกันการเข้าถึงข้อมูลสุขภาพผ่าน audit log และจัดการข้อความยืนยันแบบ asynchronous โดยไม่ให้การจองเสียหายเมื่อส่งข้อความล้มเหลว แนวทางการสร้างจะมุ่งไปที่ 3 ส่วนหลักคือ รายการว่างก่อนยืนยัน, การยืนยันและบันทึกการจอง, และการจัดการ retry + audit log ตามข้อกำหนด

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| React + Vite | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับหน้าเลือกแพ็กเกจ วัน และช่วงเวลาในการจอง |
| Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับ API ประมวลผลการจองและตรวจสอบกฎธุรกิจ |
| MySQL | CON-TECH-01 | ใช้เก็บข้อมูลการจองและข้อมูลโควตา/สถานะการจอง |
| ระบบยืนยันตัวตนที่มีอยู่ | IF-IDP-01 | ไม่สร้างฟีเจอร์ใหม่ ใช้ผลยืนยันตัวตนเป็น precondition |
| SMS/LINE notification gateway | IF-NOT-01 | ส่งแบบ asynchronous ไม่ให้การจองรอผลตอบกลับ |
| HIS integration | IF-HIS-01 | ใช้ค้นหาข้อมูลผู้รับบริการด้วยเลขบัตรประชาชนแล้วคง HN ในระบบเท่านั้น |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ FR / Constraint |
|---|---|---|
| Patient | patient_id, hn, full_name, identity_verified_at | IF-IDP-01, IF-HIS-01, FR-BKG-02, FR-BKG-04 |
| Booking | booking_id, patient_id, package_id, booking_date, slot_id, status, queue_no, created_at, confirmed_at | FR-BKG-02, FR-BKG-04, FR-BKG-05, AC-BKG-01, AC-BKG-02, AC-BKG-04 |
| BookingSlot | slot_id, date, start_time, end_time, capacity, remaining_seats, package_id | FR-BKG-01, FR-BKG-03, FR-BKG-06, AC-BKG-03, AC-BKG-05 |
| NotificationRequest | notification_id, booking_id, channel, payload, status, retry_count, next_retry_at, created_at | FR-BKG-05, NFR-REL-02, ASM-03 |
| AuditLog | audit_id, actor_id, accessed_at, patient_ref, action, resource | DOM-PDPA-01, AC-BKG-06 |
| AvailabilityView | date, slot, remaining_seats, package_id | FR-BKG-01, FR-BKG-06 |

หมายเหตุ: ไม่เก็บเลขบัตรประชาชนในตารางการจองตาม IF-HIS-01 และข้อมูลสุขภาพจะถูกบันทึก audit log ทุกครั้งตาม DOM-PDPA-01

## 4. API / หน้าจอ

- GET /api/booking/availability?packageId=&fromDate=&toDate= -> แสดงช่วงเวลาว่าง 30 วัน พร้อมจำนวนที่นั่งคงเหลือ, รองรับ FR-BKG-01
- POST /api/booking/validate -> ตรวจสิทธิ์และตรวจคิวที่ยังไม่ได้ใช้ในวันเดียวกัน, รองรับ FR-BKG-02
- POST /api/booking/slots/recommend -> ให้ 3 ตัวเลือกใกล้เคียงเมื่อช่วงเวลาที่เลือกเต็ม, รองรับ FR-BKG-03
- POST /api/booking/confirm -> บันทึกการจอง ตัดที่นั่งและสร้างหมายเลขคิว, รองรับ FR-BKG-04
- POST /api/booking/notifications/retry -> ส่งซ้ำข้อความยืนยันสูงสุด 3 ครั้งภายใน 10 นาที, รองรับ FR-BKG-05
- POST /api/booking/change-package -> คำนวณช่วงเวลาว่างใหม่ตามแพ็กเกจที่เปลี่ยน, รองรับ FR-BKG-06
- GET /api/patients/{hn}/booking-history -> ดึงข้อมูลการจองเพื่อแสดงผลบนหน้า UI ตามฐานข้อมูลภายในระบบ
- หน้า: BookingSelectionPage -> เลือกแพ็กเกจ วัน และช่วงเวลา, รองรับ FR-BKG-01, FR-BKG-06
- หน้า: BookingConfirmPage -> ยืนยันการจอง, แสดง countdown, แจ้ง “ช่วงเวลาเต็ม”, รองรับ FR-BKG-03, FR-BKG-04, NFR-USE-01
- หน้า: BookingResultPage -> แสดงหมายเลขคิวและสถานะข้อความยืนยัน, รองรับ FR-BKG-04, FR-BKG-05

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | โมเดลข้อมูล Booking, BookingSlot และไฟล์ข้อมูล MySQL; ใช้ฐานข้อมูล MySQL สำหรับข้อมูลการจองและโควตา | ใช้แล้ว |
| DOM-PDPA-01 | Entity AuditLog และหน้า/API การเข้าถึงข้อมูลผู้รับบริการ; บันทึกผู้เข้าถึง เวลา และรหัสผู้รับบริการ | ใช้แล้ว |
| IF-IDP-01 | ขั้นตอน validate ก่อนให้เรียกข้อมูลผู้รับบริการและยืนยันการจอง; ใช้ผลยืนยันตัวตนจากระบบภายนอกเป็น precondition | ใช้แล้ว |
| IF-HIS-01 | Entity Patient และข้อมูลอ้างอิง HN; ไม่เก็บเลขบัตรประชาชนในตาราง Booking | ใช้แล้ว |
| IF-NOT-01 | Entity NotificationRequest และ API retry; ข้อความส่งแบบ asynchronous และไม่ให้การจองรอผลตอบกลับ | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_booking_confirm_success | สร้าง BookingSlot มีที่นั่ง 1 ที่ในช่วง 09.00 น. หลังยืนยัน ให้ตรวจว่า booking ถูกสร้าง, queue_no แสดง, และ remaining_seats เป็น 0 |
| AC-BKG-02 | test_AC_BKG_02_reject_duplicate_active_queue_same_day | ตั้งสถานะคิว “ยังไม่ได้ใช้” สำหรับผู้รับบริการในวันเดียวกัน แล้วลองจองใหม่ ต้องถูกปฏิเสธและแสดง queue_no เดิม |
| AC-BKG-03 | test_AC_BKG_03_show_full_slot_and_alternatives | ทำให้ช่วงเวลาที่เลือกเหลือ 1 ที่ แล้วมีผู้ใช้อีกคนยืนยันก่อน ให้ตรวจว่าระบบแสดง “ช่วงเวลาเต็ม” และเสนอ 3 ตัวเลือกที่ใกล้เคียง พร้อมไม่มีการบันทึกซ้อน |
| AC-BKG-04 | test_AC_BKG_04_booking_persists_when_notification_fails | จำลอง notification gateway ล้มเหลว หลังยืนยัน จนกว่าจะแสดงหมายเลขคิวและคงบันทึกการจองไว้ พร้อมตรวจ queue retry count และเวลา retry |
| AC-BKG-05 | test_AC_BKG_05_availability_lookup_p95_under_2s | จำลองผู้ใช้พร้อมกัน 200 คนและเรียก GET /api/booking/availability ตรวจ p95 ของเวลาตอบสนองว่า <= 2 วินาที |
| AC-BKG-06 | test_AC_BKG_06_audit_log_recorded_on_access | จำลองการเข้าถึงข้อมูลการจองของผู้รับบริการ ตรวจว่า audit log มีผู้เข้าถึง เวลา และรหัสผู้รับบริการ |

## 7. ลำดับงาน

1. กำหนด schema และ migration สำหรับ Booking, BookingSlot, NotificationRequest, AuditLog พร้อม index ที่จำเป็น (รองรับ FR-BKG-01, FR-BKG-02, FR-BKG-04, DOM-PDPA-01)
2. สร้าง API ค้นหาช่วงเวลาว่างและคำนวณ remaining_seats ตามแพ็กเกจและวันที่ (รองรับ FR-BKG-01, FR-BKG-06, AC-BKG-05)
3. สร้างตรรกะตรวจ duplicate booking same day และแสดงหมายเลขคิวเดิมเมื่อปฏิเสธ (รองรับ FR-BKG-02, AC-BKG-02)
4. สร้างหน้า BookingSelectionPage และ BookingConfirmPage พร้อม countdown timer และการเสนอ 3 ตัวเลือกเมื่อเต็ม (รองรับ FR-BKG-03, NFR-USE-01, AC-BKG-03)
5. สร้าง workflow ยืนยันการจอง: transaction บันทึก booking, ลด remaining_seats, สร้าง queue_no, ส่งคำขอ notification (รองรับ FR-BKG-04, AC-BKG-01)
6. สร้าง notification queue/retry สูงสุด 3 ครั้ง ใน 10 นาที และยืนยันว่าการจองยังคงอยู่แม้ notification ล้มเหลว (รองรับ FR-BKG-05, NFR-REL-02, AC-BKG-04)
7. เพิ่ม audit log และตรวจสอบการเข้าถึงข้อมูลสุขภาพทุกครั้ง (รองรับ DOM-PDPA-01, AC-BKG-06)
8. ทดสอบระบบครบทุก AC และตรวจ performance ตาม NFR-PERF-01 (รองรับ AC-BKG-01 ถึง AC-BKG-06)

## 8. สิ่งที่ยังไม่ทำ

- ไม่มี Open Question ที่ค้างอยู่ในข้อนี้อีกต่อไป หลังจากทีมตัดสินใจแล้วว่า “ช่วงเวลาใกล้เคียง” พิจารณาเฉพาะวันเดียวกัน และหมายเลขคิวจะรีเซ็ตรายวัน

## สรุปผล

แผนนี้ยึดตาม spec.md โดยคงขอบเขตของ UC-01 ไว้ตามที่ระบุ ไม่เพิ่มฟีเจอร์นอก scope และให้ความสำคัญกับความถูกต้องของข้อมูลการจอง ความปลอดภัยตาม PDPA และการต้านทานความล้มเหลวของระบบแจ้งเตือนตาม requirement ที่ทีมกำหนดไว้
