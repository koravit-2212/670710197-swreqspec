import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import SlotPicker from '../pages/SlotPicker'

// Test for T-09: หน้าจอโหลดช่วงเวลาโดยเรียก API จำลองและแสดงรายการช่วงเวลา
test('SlotPicker loads and displays slots from API', async () => {
  const fakeSlots = [
    { id: 1, slot_date: '2026-10-01', start_time: '09:00', remaining: 5 },
    { id: 2, slot_date: '2026-10-01', start_time: '10:00', remaining: 2 },
  ]

  const mockApi = {
    getSlots: vi.fn().mockResolvedValue(fakeSlots),
  }

  render(<SlotPicker apiClient={mockApi} />)

  await waitFor(() => expect(mockApi.getSlots).toHaveBeenCalled())

  const list = screen.getByTestId('slots-list')
  expect(list).toBeTruthy()
  expect(list.children.length).toBe(2)
  const text = list.textContent || ''
  expect(text).toContain('09:00')
  expect(text).toContain('remaining: 5')
})
