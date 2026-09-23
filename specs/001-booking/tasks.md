# Tasks: จองคิวตรวจสุขภาพ (Booking)
Feature: จองคิวตรวจสุขภาพ | Spec ID: SPEC-BKG-001
อ้างอิง: plan.md | วันที่: 2569-09-22

สรุป: มี 12 งานหลัก (T-01 ถึง T-12), มี 1 งานที่รอ Open Questions (Q-02)

### T-01 สร้างตารางและ migration สำหรับ `slots`, `bookings`, `audit_logs`
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-xx
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/migrations/001_init.py, backend/app/db/session.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: สคริปต์ migration `migrations/001_init.py` รันแล้วตาราง `slots`, `bookings`, `audit_logs` ปรากฏใน engine SQLite ทดสอบ
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้าง endpoint GET /slots และ service คำนวณช่วงว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05 (test_AC_BKG_05 ย่อส่วน), ไม่มี AC หน้าที่ตรงสำหรับการคำนวณแพ็กเกจต้องเพิ่ม test หากจำเป็น
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots ตอบรายการช่วงเวลาและ `remaining` ถูกต้องเมื่อเรียกผ่าน test ที่รันใน SQLite
- สถานะ: พร้อมทำ

### T-03 สร้าง POST /bookings พื้นฐาน: สร้าง booking, ตัด remaining, บันทึก queue_no (ค่าว่างได้)
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01 (test_AC_BKG_01)
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py
- ต้องทำหลัง: T-01, (ขึ้นอยู่กับ T-02 สำหรับการเช็คความสอดคล้องถ้าต้อง)
- เสร็จเมื่อ: POST /bookings สำเร็จและ `remaining` ลดลงตาม test_AC_BKG_01
- สถานะ: พร้อมทำ

### T-04 กันจองซ้ำวันเดียวกัน (ตรวจ HN ผ่าน IF-HIS-01 และ IF-IDP-01 precondition)
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02 (test_AC_BKG_02)
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/auth/idp.py
- ต้องทำหลัง: T-01, T-03
- เสร็จเมื่อ: ผู้ใช้ที่มี booking เดิมในวันเดียวกัน ถูกปฏิเสธและได้รับ booking เดิมตาม test
- สถานะ: พร้อมทำ

### T-05 เสนอช่วงใกล้เคียงเมื่อช่วงเต็ม (409 และ 3 ตัวเลือก)
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03 (test_AC_BKG_03)
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/slots/service.py, backend/app/booking/router.py
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: เมื่อ POST /bookings เจอเต็มแล้วกลับ 409 พร้อม payload ของ 3 ช่วงที่ใกล้ที่สุดตามเงื่อนไข
- สถานะ: พร้อมทำ

### T-06 คิวส่งข้อความ: วางงานลงคิวแบบ async และนโยบายส่งซ้ำตาม ASM-03
- รองรับ: IF-NOT-01, ASM-03
- ตรวจด้วย: AC-BKG-04 (test_AC_BKG_04)
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: POST /bookings ไม่รอผลการส่งข้อความ และมีงานในคิวจำลองที่ตั้งค่าให้ส่งซ้ำภายใน 5 นาทีเมื่อจำลองพลาด
- สถานะ: พร้อมทำ

### T-07 audit log middleware บันทึกการเข้าถึงข้อมูลจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06 (test_AC_BKG_06)
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/db/models.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: การเรียกดู booking สร้าง record ใน `audit_logs` ที่มี `actor_id`, `accessed_at`, `hn`
- สถานะ: พร้อมทำ

### T-08 ค้น HN จาก HIS (interface) สำหรับ lookup ผู้ป่วย
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ (ใช้เป็นส่วนประกอบของฟีเจอร์) หากจำเป็นให้เพิ่ม test integration
- ไฟล์ที่แตะ: backend/app/his/client.py
- ต้องทำหลัง: ไม่มี (สามารถ mock ใน test)
- เสร็จเมื่อ: GET /patients/lookup ส่งต่อไปยัง HIS client และคืนค่า `hn` ตามที่ mock กำหนด
- สถานะ: พร้อมทำ

### T-09 หน้าจอ: หน้าเลือกแพ็กเกจและช่วงเวลา (ใช้ API จำลอง)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ (เป็นพื้นฐานของหน้าจอ) แต่มีการทดสอบหน้าจอสำหรับ AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: ไม่มี (ตามกฎหน้าจอเริ่มได้โดยใช้ API จำลอง)
- เสร็จเมื่อ: หน้าจอโหลดช่วงเวลาโดยเรียก API จำลองและแสดงรายการช่วงเวลา
- สถานะ: พร้อมทำ

### T-10 หน้าจอ: หน้ายืนยัน (ConfirmBooking) แสดงกรณี 409 และ 3 ตัวเลือก
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03 (AC-BKG-03.test.jsx)
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-09
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" และ 3 ปุ่มตัวเลือกตาม test
- สถานะ: พร้อมทำ

### T-11 หน้าจอ: หน้าแสดงผลการจอง (BookingResult) แสดงหมายเลขคิว แม้ส่งข้อความไม่สำเร็จ
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01 (ส่วนแสดง), AC-BKG-04 (แสดง queue และคิวส่งซ้ำเป็นงานในคิว)
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/src/__tests__/AC-BKG-04.test.jsx
- ต้องทำหลัง: T-03, T-06
- เสร็จเมื่อ: หน้าจอแสดง `queue_no` ที่ได้จาก API และยังแสดงเมื่อระบบส่งข้อความล้มเหลว
- สถานะ: พร้อมทำ

### T-12 ต่อหน้าจอกับ API จริง (เชื่อม frontend กับ backend จริง)
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ใหม่ (เป็น integration) แต่ต้องเตรียม smoke test เล็ก ๆ
- ไฟล์ที่แตะ: frontend/src/api/client.js, vite.config.js
- ต้องทำหลัง: T-02, T-03, T-05, T-06, T-09, T-10, T-11
- เสร็จเมื่อ: เมื่อหน้าจอเรียก API จริงที่รันใน Codespace และฟังก์ชันสำคัญทำงานตาม AC ที่เกี่ยวข้อง
- สถานะ: รอ Q-02

---

## ตารางตรวจความครบ

AC ID | task ที่ตรวจ AC นี้
---|---
AC-BKG-01 | T-03
AC-BKG-02 | T-04
AC-BKG-03 | T-05, T-10
AC-BKG-04 | T-06, T-11
AC-BKG-05 | T-02
AC-BKG-06 | T-07

Constraint ID | task ที่ทำให้เป็นจริง
---|---
CON-TECH-01 | T-01
DOM-PDPA-01 | T-01, T-07
IF-IDP-01 | T-04
IF-HIS-01 | T-01, T-08
IF-NOT-01 | T-06

## สิ่งที่ยังไม่ทำ (Open Questions)
- Q-02: รูปแบบหมายเลขคิว (รีเซ็ตวันต่อวันหรือนับต่อเนื่อง และรูปแบบเช่น A001?)
  - งานที่รอ: T-12 (สถานะ: รอ Q-02)

---

หมายเหตุเพิ่มเติม:
- เพิ่ม task ทดสอบสำหรับ FR-BKG-06/การเปลี่ยนแพ็กเกจยังไม่มี AC ใน spec — ถ้าทีมต้องการ ให้เพิ่ม AC และ taskทดสอบแยก
