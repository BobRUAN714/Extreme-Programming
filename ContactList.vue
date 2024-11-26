
<template>
  <div class="contact-list">
    <div class="button-group">
      <el-button type="primary" @click="showAddDialog = true">
        Add Contact
      </el-button>
      <el-button type="success" @click="exportToExcel">
        Export to Excel
      </el-button>
      <el-upload
        class="excel-uploader"
        accept=".xlsx,.xls"
        :show-file-list="false"
        :auto-upload="false"
        :on-change="handleFileChange"
      >
        <el-button type="warning">Import from Excel</el-button>
      </el-upload>
    </div>

    <el-table :data="sortedContacts" style="width: 100%; margin-top: 20px">
      <el-table-column width="70" align="center">
        <template #default="scope">
          <el-button
            :type="scope.row.important ? 'danger' : 'info'"
            :icon="Star"
            circle
            size="small"
            @click="toggleImportant(scope.row)"
          />
        </template>
      </el-table-column>
      <el-table-column prop="names" label="Names">
        <template #default="scope">
          {{ scope.row.names.join(', ') }}
        </template>
      </el-table-column>
      <el-table-column prop="phones" label="Phones">
        <template #default="scope">
          {{ scope.row.phones.join(', ') }}
        </template>
      </el-table-column>
      <el-table-column prop="emails" label="Emails">
        <template #default="scope">
          {{ scope.row.emails.join(', ') }}
        </template>
      </el-table-column>
      <el-table-column label="Operations">
        <template #default="scope">
          <el-button type="primary" size="small" @click="editContact(scope.row)">
            Edit
          </el-button>
          <el-button type="danger" size="small" @click="deleteContact(scope.row)">
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      :title="editingContact ? 'Edit Contact' : 'Add Contact'"
      v-model="showAddDialog"
      width="600px"
    >
      <el-form :model="currentContact" label-width="100px">
        <!-- Important Switch -->
        <el-form-item label="Important">
          <el-switch v-model="currentContact.important" />
        </el-form-item>

        <!-- Names -->
        <el-form-item label="Names">
          <div v-for="(name, index) in currentContact.names" :key="'name'+index" class="input-with-delete">
            <el-input v-model="currentContact.names[index]" placeholder="Enter name" />
            <el-button type="danger" circle @click="removeItem('names', index)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
          <el-button type="primary" plain @click="addItem('names')" style="margin-top: 10px">
            Add Another Name
          </el-button>
        </el-form-item>

        <!-- Phones -->
        <el-form-item label="Phones">
          <div v-for="(phone, index) in currentContact.phones" :key="'phone'+index" class="input-with-delete">
            <el-input v-model="currentContact.phones[index]" placeholder="Enter phone number" />
            <el-button type="danger" circle @click="removeItem('phones', index)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
          <el-button type="primary" plain @click="addItem('phones')" style="margin-top: 10px">
            Add Another Phone
          </el-button>
        </el-form-item>

        <!-- Emails -->
        <el-form-item label="Emails">
          <div v-for="(email, index) in currentContact.emails" :key="'email'+index" class="input-with-delete">
            <el-input v-model="currentContact.emails[index]" placeholder="Enter email" />
            <el-button type="danger" circle @click="removeItem('emails', index)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
          <el-button type="primary" plain @click="addItem('emails')" style="margin-top: 10px">
            Add Another Email
          </el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">Cancel</el-button>
        <el-button type="primary" @click="saveContact">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { Star } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx'
import FileSaver from 'file-saver'
import 'element-plus/dist/index.css'
interface Contact {
  id?: number
  names: string[]
  phones: string[]
  emails: string[]
  important: boolean
}

const contacts = ref<Contact[]>([])
const showAddDialog = ref(false)
const editingContact = ref<Contact | null>(null)
const currentContact = ref<Contact>({
  names: [''],
  phones: [''],
  emails: [''],
  important: false
})

// 排序联系人，重要联系人排在前面
const sortedContacts = computed(() => {
  return [...contacts.value].sort((a, b) => {
    if (a.important && !b.important) return -1
    if (!a.important && b.important) return 1
    return 0
  })
})

// 切换重要状态
const toggleImportant = (contact: Contact) => {
  const index = contacts.value.findIndex(c => c.id === contact.id)
  if (index > -1) {
    contacts.value[index].important = !contacts.value[index].important
    ElMessage.success(`Contact marked as ${contacts.value[index].important ? 'important' : 'normal'}`)
  }
}

// 添加新的输入项
const addItem = (field: 'names' | 'phones' | 'emails') => {
  currentContact.value[field].push('')
}

// 删除输入项
const removeItem = (field: 'names' | 'phones' | 'emails', index: number) => {
  if (currentContact.value[field].length > 1) {
    currentContact.value[field].splice(index, 1)
  } else {
    ElMessage.warning('At least one item is required')
  }
}

// 编辑联系人
const editContact = (contact: Contact) => {
  editingContact.value = contact
  currentContact.value = JSON.parse(JSON.stringify(contact)) // Deep copy
  showAddDialog.value = true
}

// 删除联系人
const deleteContact = (contact: Contact) => {
  const index = contacts.value.findIndex(c => c.id === contact.id)
  if (index > -1) {
    contacts.value.splice(index, 1)
    ElMessage.success('Contact deleted successfully')
  }
}

// 保存联系人
const saveContact = () => {
  // 验证至少有一个非空值
  if (!currentContact.value.names[0] || !currentContact.value.phones[0] || !currentContact.value.emails[0]) {
    ElMessage.error('Please fill in at least one name, phone and email')
    return
  }

  if (editingContact.value) {
    // 更新现有联系人
    const index = contacts.value.findIndex(c => c.id === editingContact.value?.id)
    if (index > -1) {
      contacts.value[index] = { ...currentContact.value }
    }
  } else {
    // 添加新联系人
    contacts.value.push({
      ...currentContact.value,
      id: Date.now()
    })
  }
  showAddDialog.value = false
  editingContact.value = null
  currentContact.value = { names: [''], phones: [''], emails: [''], important: false }
  ElMessage.success('Contact saved successfully')
}

// 导出到Excel
const exportToExcel = () => {
  try {
    const exportData = contacts.value.map(contact => {
      return {
        'Important': contact.important ? 'Yes' : 'No',
        'Names': contact.names.join('; '),
        'Phones': contact.phones.join('; '),
        'Emails': contact.emails.join('; ')
      }
    })

    const wb = XLSX.utils.book_new()
    const ws = XLSX.utils.json_to_sheet(exportData)

    const colWidths = [
      { wch: 10 }, // Important
      { wch: 30 }, // Names
      { wch: 30 }, // Phones
      { wch: 40 }  // Emails
    ]
    ws['!cols'] = colWidths

    XLSX.utils.book_append_sheet(wb, ws, 'Contacts')

    const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
    const data = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })

    FileSaver.saveAs(data, `contacts_${new Date().toISOString().split('T')[0]}.xlsx`)

    ElMessage.success('Contacts exported successfully')
  } catch (error) {
    console.error('Export failed:', error)
    ElMessage.error('Failed to export contacts')
  }
}

// 处理文件导入
const handleFileChange = async (file: any) => {
  try {
    const data = await file.raw.arrayBuffer()
    const workbook = XLSX.read(data)
    const worksheet = workbook.Sheets[workbook.SheetNames[0]]
    const jsonData = XLSX.utils.sheet_to_json(worksheet)

    const importedContacts: Contact[] = jsonData.map((row: any) => ({
      id: Date.now() + Math.random(),
      names: row['Names']?.split(';').map((name: string) => name.trim()) || [''],
      phones: row['Phones']?.split(';').map((phone: string) => phone.trim()) || [''],
      emails: row['Emails']?.split(';').map((email: string) => email.trim()) || [''],
      important: row['Important']?.toLowerCase() === 'yes'
    }))

    const validContacts = importedContacts.filter(contact =>
      contact.names[0] && contact.phones[0] && contact.emails[0]
    )

    if (validContacts.length === 0) {
      ElMessage.error('No valid contacts found in the file')
      return
    }

    contacts.value.push(...validContacts)

    ElMessage.success(`Successfully imported ${validContacts.length} contacts`)
  } catch (error) {
    console.error('Import failed:', error)
    ElMessage.error('Failed to import contacts. Please check your file format.')
  }
}
</script>

<style scoped>
.contact-list {
  padding: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.input-with-delete {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.el-button.is-circle {
  padding: 8px;
}

.excel-uploader {
  display: inline-block;
}
</style>
