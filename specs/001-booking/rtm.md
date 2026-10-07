# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:35 | test: 8 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 | T-02 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | test_AC_BKG_05: ผ่าน | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | ไม่มีการปฏิเสธจองซ้ำใน backend/app/booking/service.py: create_booking | ไม่มี test | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ไม่มีข้อเสนอช่วงใกล้เคียง 3 ช่วงในโค้ด | ไม่มี test | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/router.py: create_booking; backend/app/booking/service.py: create_booking; backend/app/booking/service.py: next_queue_no | test_AC_BKG_01: ผ่าน | รอ Q-xx |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มีคิวจัดส่งข้อความซ้ำในโค้ด | ไม่มี test | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-10 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | ไม่มี test | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | test_AC_BKG_05: ผ่าน | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี | ไม่มีการตั้งค่าการเข้ารหัส TLS ในโค้ด | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มีคิวส่งซ้ำ/นโยบาย retry ในโค้ด | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี | ไม่มีโค้ดหรือ test สำหรับประสิทธิภาพผู้ใช้ใหม่ 8/10 คน | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py; backend/app/db/session.py | ไม่มี test เฉพาะค่า DATABASE_URL แต่ test schema ผ่าน | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 | backend/app/db/models.py: AuditLog เท่านั้น; ไม่มี middleware หรือการบันทึก audit log ใน request | ไม่มี test | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py: get_verified_hn; backend/app/booking/router.py: create_booking | test_AC_BKG_01: ผ่าน | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 | backend/app/db/models.py: Booking เก็บเฉพาะ hn; ไม่มี HIS lookup และไม่มีการแข่งขันตรวจสอบ national_id | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ไม่มีคิวส่งข้อความ async / retry ในโค้ด | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/router.py: get_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | คืนรายการช่วงเวลาที่ยังมี slot แต่ไม่จำกัดให้แสดงได้ภายใน 30 วัน ข้างหน้า และไม่ได้กรองเพียง remaining > 0 |
| backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ใช้ DAYS_AHEAD = 14 แทน 30 วัน และไม่มีการกรอง slot ที่ remaining <= 0 ตามข้อกำหนดช่วงเวลาว่าง |
| backend/app/booking/router.py: create_booking | FR-BKG-04, IF-IDP-01 | ครึ่งหนึ่ง | ตรวจ token ก่อนจองได้ แต่ไม่มีการปฏิเสธการจองซ้ำวันเดียวกันหรือแสดง queue format ตาม Q-02 |
| backend/app/booking/service.py: create_booking | FR-BKG-02, FR-BKG-04 | ไม่ครบ | แทนที่จะปฏิเสธคิวซ้ำวันเดียวกัน มันลด remaining ทันทีโดยไม่ตรวจการจองที่มีอยู่ |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ครบ | ตรวจ token รูปแบบ Bearer verified:<HN> ตามแนวทางจำลองของระบบยืนยันตัวตน |
| backend/app/db/models.py: Slot / Booking / AuditLog | FR-BKG-04, IF-HIS-01, DOM-PDPA-01 | ครึ่งหนึ่ง | เก็บ hn เท่านั้นและมี AuditLog table แต่ไม่มี audit middleware หรือ log request จริง |
| frontend/src/api/client.js | FR-BKG-01, FR-BKG-03 | ไม่ครบ | ต่อ API slot และ booking แต่ไม่ใช่หน้า UI ของ AC จริง และไม่มี test สำหรับ UI ตาม spec |
| frontend/src/App.jsx | ไม่มี ID หลัก | ไม่ครบ | เป็นโครงหน้าเริ่มต้น ไม่มีหน้าเลือกวัน/ช่วงเวลา/ยืนยันการจองตาม FR-BKG-01 / FR-BKG-03 |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py: list_available_slots | FR-BKG-01 | ใช้ DAYS_AHEAD = 14 แทน 30 วันข้างหน้า และไม่กรอง slot ที่ remaining <= 0 ดังนั้นรายการที่ส่งกลับไม่ได้สอดคล้องกับคำว่า “ช่วงเวลาที่ว่าง” ตาม spec |  |
| F-002 | FR ไม่มี AC | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | FR-BKG-06 | FR-BKG-06 ระบุการคำนวณช่วงเวลาว่างตามแพ็กเกจ แต่ไม่มี AC ที่ตรวจว่าเปลี่ยนแพ็กเกจแล้วข้อมูลมีการอัปเดตจริงหรือไม่ ทำให้ขาด traceability จาก requirement ไป test |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ไม่มี | ไม่มีข้อค้นพบเก่าที่ AI ตรวจแล้วและยืนยันว่าแก้แล้วในรอบนี้ |
