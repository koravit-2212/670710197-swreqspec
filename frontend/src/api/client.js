// จุดเดียวที่หน้าจอใช้เรียก API หลังบ้าน (ตามสัญญา API ใน plan.md ข้อ 4)
// ตอน test ให้ส่ง client จำลองเข้าไปในหน้าจอแทน ไม่ต้องรันหลังบ้านจริง
// เรียกผ่าน /api (ดู proxy ใน vite.config.js) หลังบ้านต้องรันอยู่ที่ port 8000
const BASE = import.meta.env.VITE_API_BASE ?? '/api'
const USE_MOCK = import.meta.env.VITE_API_MOCK === 'true'

export const api = {
  async getSlots({ dateFrom, packageCode } = {}) {
    if (USE_MOCK) {
      // Mock data for frontend development (used when VITE_API_MOCK=true)
      return [
        { id: 1, slot_date: '2026-10-01', start_time: '09:00', remaining: 5 },
        { id: 2, slot_date: '2026-10-01', start_time: '10:00', remaining: 2 },
      ]
    }
    const q = new URLSearchParams({ date_from: dateFrom, package_code: packageCode })
    const res = await fetch(`${BASE}/slots?${q}`)
    return res.json()
  },
  async createBooking({ slotId }) {
    if (USE_MOCK) {
      return { status: 201, body: { id: 123, queue_no: '0001' } }
    }
    const res = await fetch(`${BASE}/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slot_id: slotId }),
    })
    return { status: res.status, body: await res.json() }
  },
}
