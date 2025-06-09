<template>
    <div class="flex gap-6 overflow-x-auto pb-6">
      <draggable
        :list="statuses"
        group="statuses"
        class="flex gap-6"
        @end="onStatusReorder"
        item-key="id"
        :animation="300"
      >
        <template #item="{ element: status }">
          <section
            class="w-80 rounded-md p-5 shadow-md flex flex-col"
            :style="{ backgroundColor: status.color || '#ffffff' }"
          >
            <header class="flex justify-between items-center mb-4">
              <h2
                class="text-xl font-semibold truncate"
                :style="{ color: getTextColor(status.color) }"
              >
                {{ status.name }}
              </h2>
              <button
                @click="removeStatus(status.id)"
                class="text-red-400 hover:text-red-600 text-2xl"
                title="Remove Status"
              >
                &times;
              </button>
            </header>
            <draggable
              :list="tasksByStatus(status.id)"
              group="tasks"
              @end="onTaskReorder"
              class="flex-1 space-y-4 overflow-y-auto"
              item-key="id"
              :animation="250"
            >
              <template #item="{ element: task }">
                <TaskCard
                  :task="task"
                  @update-task="handleInlineUpdate"
                  class="cursor-move hover:scale-105 transition-transform duration-200"
                  :style="{ backgroundColor: task.color || '#f0f0f0' }"
                  :text-color="getTextColor(task.color)"
                />
              </template>
            </draggable>
            <button
              @click="openNewTaskForm(status.id)"
              class="mt-5 py-2 px-4 rounded-md bg-gradient-to-r from-green-400 to-blue-500 text-white font-medium hover:from-green-500 hover:to-blue-600 transition duration-300"
            >
              + New Task
            </button>
          </section>
        </template>
      </draggable>

      <!-- Add Status Column -->
      <section class="w-64 flex-shrink-0">
        <div v-if="!addingStatus" class="h-full flex items-center justify-center">
          <button
            @click="startAddStatus"
            class="w-full h-48 p-4 border-2 border-dashed border-gray-300 rounded-md text-gray-600 font-medium hover:border-gray-400 hover:bg-white transition"
          >
            + Add Status
          </button>
        </div>
        <div v-else class="bg-white p-5 rounded-md shadow-md">
          <input
            v-model="newStatusName"
            type="text"
            placeholder="Enter status title"
            class="w-full p-3 border-b border-gray-300 focus:outline-none focus:border-blue-500 mb-4 text-base font-medium"
          />
          <div class="flex items-center space-x-3 mb-3">
            <label class="font-medium text-gray-700">Color:</label>
            <input
              type="color"
              v-model="newStatusColor"
              class="w-8 h-8 rounded"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button
              @click="cancelAddStatus"
              class="px-3 py-2 text-gray-600 font-medium hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              @click="confirmAddStatus"
              class="px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 transition disabled:opacity-50"
              :disabled="statusLoading || !newStatusName.trim()"
            >
              <span v-if="statusLoading">Adding...</span>
              <span v-else>Add</span>
            </button>
          </div>
        </div>
      </section>
    </div>

    <!-- New Task Form Modal -->
    <div
      v-if="showTaskForm"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50"
    >
      <div class="bg-white w-full max-w-lg p-8 rounded-md shadow-xl">
        <h3 class="text-2xl font-bold mb-6 text-gray-900">Create New Task</h3>
        <form @submit.prevent="handleCreateTask" class="space-y-5">
          <div>
            <label class="block mb-1 font-medium text-gray-700" for="title">Title</label>
            <input
              v-model="newTask.title"
              id="title"
              type="text"
              placeholder="Task title"
              class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-base"
              required
            />
          </div>
          <div>
            <label class="block mb-1 font-medium text-gray-700" for="description">Description</label>
            <textarea
              v-model="newTask.description"
              id="description"
              rows="3"
              placeholder="Task description"
              class="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 text-base resize-none"
            ></textarea>
          </div>
          <div class="flex items-center space-x-3">
            <label class="font-medium text-gray-700">Color:</label>
            <input
              type="color"
              v-model="newTask.color"
              class="w-8 h-8 rounded"
            />
          </div>
          <div class="flex justify-end space-x-4 mt-6">
            <button
              type="button"
              @click="showTaskForm = false"
              class="px-5 py-2 font-medium text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700"
            >
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import draggable from 'vuedraggable'
import TaskCard from './TaskCard.vue'

export default {
  name: 'KanbanBoard',
  components: { TaskCard, draggable },
  props: { projectId: { type: Number, required: true } },
  data() {
    return {
      showTaskForm: false,
      newTask: { title: '', description: '', status_id: null, color: '#f0f0f0' },
      addingStatus: false,
      newStatusName: '',
      newStatusColor: '#ffffff',
      statusLoading: false
    }
  },
  computed: {
    ...mapState('tasks', ['tasks', 'statuses']),
    tasksByStatus() {
      return statusId => this.tasks.filter(task => task.status.id === statusId)
    }
  },
  methods: {
    ...mapActions('tasks', ['fetchTasks', 'fetchStatuses', 'updateTask', 'createTask', 'createStatus', 'updateStatus', 'deleteStatus']),
    loadData() {
      this.fetchStatuses(this.projectId)
      this.fetchTasks(this.projectId)
    },
    async onStatusReorder(evt) {
      const updates = this.statuses.map((s, idx) => ({ id: s.id, order: idx }))
      for (const u of updates) {
        await this.updateStatus({ statusId: u.id, payload: { order: u.order } })
      }
      this.fetchStatuses(this.projectId)
    },
    async onTaskReorder(evt) {
      const task = evt.item.__draggable_context.element
      const newStatusId = evt.to.__vueParentComponent.props.element.id
      if (task.status.id !== newStatusId) {
        await this.updateTask({ taskId: task.id, payload: { status_id: newStatusId } })
        this.fetchTasks(this.projectId)
      }
    },
    async handleInlineUpdate(updatedTask) {
      await this.updateTask({ taskId: updatedTask.id, payload: { title: updatedTask.title, description: updatedTask.description } })
      this.fetchTasks(this.projectId)
    },
    startAddStatus() {
      this.addingStatus = true
      this.newStatusName = ''
      this.newStatusColor = '#ffffff'
    },
    cancelAddStatus() {
      this.addingStatus = false
      this.newStatusName = ''
      this.newStatusColor = '#ffffff'
    },
    async confirmAddStatus() {
      if (!this.newStatusName.trim()) return
      this.statusLoading = true
      await this.createStatus({
        name: this.newStatusName,
        color: this.newStatusColor,
        projectId: this.projectId,
        order: this.statuses.length
      })
      this.newStatusName = ''
      this.newStatusColor = '#ffffff'
      this.addingStatus = false
      this.statusLoading = false
      this.fetchStatuses(this.projectId)
    },
    async removeStatus(statusId) {
      await this.deleteStatus( statusId )
      this.fetchStatuses(this.projectId)
      this.fetchTasks(this.projectId)
    },
    openNewTaskForm(statusId) {
      this.newTask = { title: '', description: '', status_id: statusId, color: '#f0f0f0' }
      this.showTaskForm = true
    },
    async handleCreateTask() {
      await this.createTask({
        title: this.newTask.title,
        description: this.newTask.description,
        projectId: this.projectId,
        status_id: this.newTask.status_id,
        color: this.newTask.color || '#f0f0f0'
      })
      this.showTaskForm = false
      this.fetchTasks(this.projectId)
    },
    getTextColor(bgColor) {
      if (!bgColor) return '#000000'
      const c = bgColor.substring(1)
      const rgb = parseInt(c, 16)
      const r = (rgb >> 16) & 0xff
      const g = (rgb >> 8) & 0xff
      const b = rgb & 0xff
      const luminance = 0.299 * r + 0.587 * g + 0.114 * b
      return luminance > 186 ? '#000000' : '#ffffff'
    }
  },
  created() {
    this.loadData()
  }
}
</script>

<style scoped>
.flex-1::-webkit-scrollbar {
  width: 6px;
}
.flex-1::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}
</style>
