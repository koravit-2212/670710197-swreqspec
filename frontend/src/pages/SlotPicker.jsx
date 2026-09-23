import React, { useEffect, useState } from 'react'
import { api } from '../api/client'

// รองรับ: FR-BKG-01, FR-BKG-06
export default function SlotPicker({ apiClient = api }) {
  const [dateFrom, setDateFrom] = useState(new Date().toISOString().slice(0, 10))
  const [packageCode, setPackageCode] = useState('STD')
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    apiClient
      .getSlots({ dateFrom, packageCode })
      .then((data) => {
        if (mounted) setSlots(data || [])
      })
      .finally(() => mounted && setLoading(false))
    return () => (mounted = false)
  }, [dateFrom, packageCode, apiClient])

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-lg font-semibold text-teal-800">เลือกแพ็กเกจและช่วงเวลา</h2>
      <div className="mt-4 grid grid-cols-12 gap-4 items-end">
        <div className="col-span-6">
          <label className="block text-sm text-slate-600 mb-1">แพ็กเกจ</label>
          <select
            data-testid="package"
            value={packageCode}
            onChange={(e) => setPackageCode(e.target.value)}
            className="w-full border rounded px-3 py-2"
          >
            <option value="STD">พรีเมียมพื้นฐาน</option>
            <option value="FULL">Full</option>
          </select>
        </div>
        <div className="col-span-6">
          <label className="block text-sm text-slate-600 mb-1 text-right">วันที่เริ่มต้น</label>
          <input
            data-testid="date-from"
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            className="w-full border rounded px-3 py-2"
          />
        </div>
      </div>

      <div className="mt-6 flex items-center justify-between">
        <h3 className="text-sm font-medium">ช่วงเวลา</h3>
        <div className="text-sm text-slate-500">{slots.length} ช่วงเวลา</div>
      </div>

      <div className="mt-3">
        {loading ? (
          <div>Loading...</div>
        ) : slots.length === 0 ? (
          <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-slate-500">
            ยังไม่มีช่วงเวลาให้เลือกสำหรับเงื่อนไขนี้
          </div>
        ) : (
          <ul data-testid="slots-list" className="space-y-2 mt-2">
            {slots.map((s) => (
              <li key={`${s.id}`} className="p-3 border rounded">
                <div className="font-medium">{s.slot_date} {s.start_time}</div>
                <div className="text-sm text-slate-500">เหลือ {s.remaining} ที่นั่ง</div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
