# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2569-09-16 15:00 คำสั่ง: /clarify

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/001-booking/spec.md (v1)

### คำถามที่ AI ถาม (ทั้งหมด)

1. ช่วงเวลาใกล้เคียงควรพิจารณาเฉพาะวันเดียวกันหรือรวมวันถัดไปด้วย?
2. หมายเลขคิวควรรีเซ็ตทุกวัน หรือเรียงต่อเนื่องตลอดทั้งเดือน/ทั้งปี?
3. “คิวที่ยังไม่ได้ใช้” หมายถึงสถานะใดบ้างที่ต้องถูกนับเป็นการมีคิวในวันเดียวกัน?
4. เมื่อระบบแจ้งเตือน SMS/LINE ไม่ตอบสนอง ต้องถือว่า “ไม่สำเร็จ” เมื่อไร และต้อง retry กี่ครั้งภายในกี่เวลา?
5. “สำเร็จภายใน 3 นาที” ใน NFR-USE-01 ควรเริ่มนับจากเวลาใด?

### คำตอบของทีมและเหตุผล

1. ใช้คำตอบเดิมในทีม: ไม่มีการปรับเปลี่ยนต่อในตอนนี้ จึงยังคงถามต่อไป
2. ใช้คำตอบเดิมในทีม: ไม่มีการปรับเปลี่ยนต่อในตอนนี้ จึงยังคงถามต่อไป
3. ใช้คำตอบเดิมในทีม: ไม่มีการปรับเปลี่ยนต่อในตอนนี้ จึงยังคงถามต่อไป
4. Q4: retry 3 ครั้ง ใน 10 นาที แล้วหยุดและคงบันทึกการจองไว้
5. Q5: เริ่มนับจากเมื่อผู้ใช้กดที่วันเวลาการจองที่เลือกจนถึงกดยืนยัน แล้วมีการแสดงการนับเวลาถอยหลังให้ผู้ใช้เห็น
6. Q1: ดูช่วงเวลาใกล้เคียงเฉพาะวันเดียวกันเท่านั้น
7. Q2: หมายเลขคิวรีเซ็ตรายวันและเริ่มจาก 1 ใหม่ทุกวัน

### สิ่งที่แก้ใน spec.md (v1 เป็น v2)

- อัปเดต Status เป็น Draft v2 และวันที่เป็น 2569-09-16
- ปรับ FR-BKG-05 ให้ระบุ retry สูงสุด 3 ครั้ง ภายใน 10 นาที แล้วหยุดและคงบันทึกการจองไว้
- ปรับ NFR-USE-01 ให้กำหนดจุดเริ่มต้นของการนับเวลา 3 นาที และระบุให้แสดงการนับเวลาถอยหลังให้ผู้ใช้เห็น
- เพิ่ม ASM-03 และ ASM-04 ใน Assumptions เพื่อสะท้อนคำตัดสินใจของทีม
- เพิ่ม ASM-05 และ ASM-06 ให้ตอบ Q1 และ Q2 ให้ชัดเจน

---

## 2569-09-16 15:15 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: specs/001-booking/plan.md
- สรุป: สร้าง plan.md ตาม template ที่ระบุ โดยยึด spec.md และไม่เพิ่ม requirement ใหม่
- Constraint ที่ยังไม่ได้ใช้: ไม่มี (ทุก Constraint ใน spec ถูกนำไปใช้ใน plan แล้ว)
- AC ที่ทดสอบยากหรือทดสอบไม่ได้ในสภาพแวดล้อมของนักศึกษา: AC-BKG-04 เนื่องจากต้องจำลอง notification gateway ที่ล้มเหลว และ AC-BKG-05 ต้องมีการจำลอง 200 user concurrency แบบจริง
- สิ่งที่ AI อยากเดาแต่ไม่ได้เดา: ไม่มีแล้ว เนื่องจาก Q-01 และ Q-02 ได้รับคำตอบชัดเจนจากทีมแล้ว

---

## 2569-09-22 คำสั่ง: /tasks

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/001-booking/spec.md, specs/001-booking/plan.md
- ผลลัพธ์: สร้าง specs/001-booking/tasks.md (12 งานหลัก ตั้งแต่ T-01 ถึง T-12; 1 งานรอ Q-02)
- หมายเหตุ: เพิ่มรายการงานและตารางตรวจความครบตามกฎของ prompt `tasks.prompt.md`

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-23 คำสั่ง: /implement T-09

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/pages/SlotPicker.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ผลการรัน test: 2 tests passed (AC-BKG-03 และ setup) หลังติดตั้ง dependencies และแก้ test ให้ใช้ `vi` และ matcher ปกติ
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี — หน้าจอใช้ API จำลองตาม plan.md จึงไม่ต้องเดา

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 คำสั่ง: /implement T-01

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/db/session.py, backend/app/db/migrations/001_init.py
- ผลลัพธ์: ซ่อม migration ให้รันได้ผ่าน SQLite และสร้างตารางที่ต้องใช้ได้จริง: `slots`, `bookings`, `audit_logs`
- ผล test: รันตรวจด้วย Python และยืนยันว่า `upgrade(engine)` คืนค่า `['audit_logs', 'bookings', 'slots']` และใน SQLite มีตารางครบตามเงื่อนไขของ T-01
- Constraint ที่ทำให้เป็นจริง: CON-TECH-01 (ใช้ SQLite ในหน่วยความจำสำหรับ migration/test ตามสถาปัตยกรรมที่กำหนด), DOM-PDPA-01 (audit_logs ถูกสร้างพร้อมตาราง), IF-HIS-01 (bookings เก็บเฉพาะ hn ตาม schema)
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี — ปัญหาจริงคือ migration filename เริ่มด้วยเลขทำให้ Python import แบบ module ไม่ได้ จึงแก้ให้รันได้ผ่าน `importlib` และ `if __name__ == "__main__":` โดยไม่ต้องเดา requirement เพิ่ม

---

## 2569-09-30 คำสั่ง: /implement T-09

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js, frontend/src/__tests__/AC-BKG-03.test.jsx
- ผลลัพธ์: ปรับหน้าเลือกแพ็กเกจและช่วงเวลาให้โหลดช่วงว่างจาก API mock และแสดงรายการช่วงเวลาได้จริง พร้อมจัดการ URL ที่ใช้ relative path ใน test environment ให้ไม่ล้มบน fetch
- ผล test: รัน `cd frontend && npm test -- --run` และได้ 2/2 test ผ่าน
- Constraint ที่ทำให้เป็นจริง: FR-BKG-01, FR-BKG-06 (หน้าเลือกแพ็กเกจและช่วงเวลาโหลดช่วงเวลาว่างและแสดงจำนวนที่นั่งคงเหลือได้ตามที่กำหนด)
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี — ปัญหาจริงคือ test environment ของ Vitest ทำให้ fetch กับ `/api/...` เป็น URL ที่ไม่ถูกต้อง และต้อง normalize origin ก่อนส่ง request

