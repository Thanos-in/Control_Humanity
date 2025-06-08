<template>
  <div class="p-8 bg-gradient-to-br from-gray-100 to-gray-200 min-h-screen">
    <!-- Status columns container with draggable -->
    <div class="flex gap-8 overflow-x-auto pb-6">
      <draggable
        :list="statuses"
        group="statuses"
        class="flex gap-8"
        @end="onStatusReorder"
        item-key="id"
        :animation="300"
      >
        <template #item="{ element: status }">
          <section class="w-80 bg-white rounded-3xl p-6 shadow-lg transform hover:-translate-y-1 transition-all duration-300 flex flex-col">
            <header class="flex justify-between items-center mb-5">
              <h2 class="text-2xl font-bold text-gray-900 truncate">{{ status.name }}</h2>
              <button @click="removeStatus(status.id)" class="text-red-400 hover:text-red-600 text-3xl leading-none">&times;</button>
            </header>
            <!-- Task list as draggable -->
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
                  class="cursor-move hover:scale-105 transform transition-transform duration-200"
                />
              </template>
            </draggable>
            <button
              @click="openNewTaskForm(status.id)"
              class="mt-6 py-3 rounded-full bg-gradient-to-r from-green-400 to-blue-500 text-white font-semibold hover:from-green-500 hover:to-blue-600 shadow-md transition-all duration-300"
            >
              + New Task
            </button>
          </section>
        </template>
      </draggable>

      <!-- Add Status Column -->
      <section class="w-80 flex-shrink-0">
        <div v-if="!addingStatus" class="h-full flex items-center justify-center">
          <button
            @click="startAddStatus"
            class="w-full h-full p-6 border-4 border-dashed border-gray-300 rounded-3xl text-gray-600 font-semibold hover:border-gray-400 hover:bg-white transition-all duration-300"
          >
            + Add Status
          </button>
        </div>
        <div v-else class="bg-white p-6 rounded-3xl shadow-lg">
          <input
            v-model="newStatusName"
            type="text"
            placeholder="Enter status title"
            class="w-full p-3 border-b-2 border-gray-300 focus:outline-none focus:border-blue-500 mb-6 text-lg font-medium"
          />
          <div class="flex justify-end space-x-4">
            <button @click="cancelAddStatus" class="px-4 py-2 text-gray-600 font-medium hover:text-gray-800 transition-all duration-200">
              Cancel
            </button>
            <button
              @click="confirmAddStatus"
              class="px-4 py-2 bg-gradient-to-r from-green-500 to-green-700 text-white font-medium rounded-full hover:from-green-600 hover:to-green-800 shadow transition-all duration-200 disabled:opacity-50"
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
      <div class="bg-white w-full max-w-lg p-10 rounded-3xl shadow-2xl">
        <h3 class="text-3xl font-bold mb-8 text-gray-900">Create New Task</h3>
        <form @submit.prevent="handleCreateTask" class="space-y-6">
          <div>
            <label class="block mb-2 font-medium text-gray-700" for="title">Title</label>
            <input
              v-model="newTask.title"
              id="title"
              type="text"
              placeholder="Task title"
              class="w-full p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg"
              required
            />
          </div>
          <div>
            <label class="block mb-2 font-medium text-gray-700" for="description">Description</label>
            <textarea
              v-model="newTask.description"
              id="description"
              rows="4"
              placeholder="Task description"
              class="w-full p-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg resize-none"
            ></textarea>
          </div>
          <div class="flex justify-end space-x-6 mt-8">
            <button
              type="button"
              @click="showTaskForm = false"
              class="px-8 py-3 font-medium text-gray-600 hover:text-gray-800 transition-all duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-8 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-all duration-200"
            >
              Create Task
            </button>
          </div>
        </form>
      </div>
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
      newTask: { title: '', description: '', status_id: null },
      addingStatus: false,
      newStatusName: '',
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
      this.addingStatus = true; this.newStatusName = ''
    },
    cancelAddStatus() {
      this.addingStatus = false; this.newStatusName = ''
    },
    async confirmAddStatus() {
      if (!this.newStatusName.trim()) return
      this.statusLoading = true
      await this.createStatus({ name: this.newStatusName, project_id: this.projectId, order: this.statuses.length })
      this.newStatusName = '';
      this.addingStatus = false;
      this.fetchStatuses(this.projectId)
      this.statusLoading = false
    },
    async removeStatus(statusId) {
      await this.deleteStatus({ statusId })
      this.fetchStatuses(this.projectId)
      this.fetchTasks(this.projectId)
    },
    openNewTaskForm(statusId) {
      this.newTask = { title: '', description: '', status_id: statusId }
      this.showTaskForm = true
    },
    async handleCreateTask() {
      await this.createTask({ title: this.newTask.title, description: this.newTask.description, project_id: this.projectId, status_id: this.newTask.status_id })
      this.showTaskForm = false
      this.fetchTasks(this.projectId)
    }
  },
  created() {
    this.loadData()
  }
}
</script>

<style scoped>
/* Custom scrollbar for status lists */
.draggable .flex-1::-webkit-scrollbar {
  width: 6px;
}
.draggable .flex-1::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
  border-radius: 3px;
}
</style>