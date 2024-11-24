import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export interface Contact {
  id?: number
  name: string
  phone: string
  email: string
}

export const contactApi = {
  // 获取所有联系人
  getContacts: () => api.get<Contact[]>('/contacts/'),
  
  // 添加联系人
  addContact: (contact: Contact) => api.post<Contact>('/contacts/', contact),
  
  // 更新联系人
  updateContact: (id: number, contact: Contact) => api.put<Contact>(`/contacts/${id}`, contact),
  
  // 删除联系人
  deleteContact: (id: number) => api.delete(`/contacts/${id}`)
}