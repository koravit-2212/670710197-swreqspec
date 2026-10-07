# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Slot
from tests.conftest import AUTH


def test_AC_BKG_01(client, db, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    payload = res.json()
    assert payload["slot_id"] == slot.id
    assert payload["queue_no"]
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_1_booking_success(client, db, make_slot):
    """TC-BKG-01-1: ยืนยันตัวตนแล้ว มีที่นั่งว่าง 1 ที่ จองสำเร็จต้องบันทึกและลด remaining เป็น 0"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    payload = res.json()
    assert payload["slot_id"] == slot.id
    assert payload["queue_no"]
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_2_remaining_goes_to_zero(client, db, make_slot):
    """TC-BKG-01-2: เมื่อช่วง 09.00 มีที่ว่างสุดท้าย 1 ที่ หลังยืนยันต้องเหลือ 0 โดยไม่ติดลบ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    assert res.json()["queue_no"]
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_3_unverified_user(client, make_slot):
    """TC-BKG-01-3: ยังไม่ได้ยืนยันตัวตน (รอ Q-xx)"""
    # Given: ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง โดยไม่ส่ง Authorization header
    client.post("/bookings", json={"slot_id": slot.id})

    # Then: spec ไม่ได้บอกว่าต้องปฏิเสธ/คืนข้อผิดพลาด/หรือบันทึกต่อเมื่อยังไม่ได้ยืนยันตัวตน (รอ Q-xx)
    # ยังไม่ตรวจเพราะรอ Q-xx
