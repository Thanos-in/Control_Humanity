<template>
    <!-- <h1>{{ project.name }}</h1> -->
    <!-- <p>{{ project.description }}</p> -->

    <!-- Kanban board -->
    <KanbanBoard :projectId="projectId" />
</template>

<script>
import { mapState, mapActions } from 'vuex'
import KanbanBoard from '../tasks/KanbanBoard.vue'

export default {
  name: 'ProjectDetail',
  components: { KanbanBoard },
  data() {
    return {
      project: {}
    }
  },
  computed: {
    projectId() {
      return parseInt(this.$route.params.id)
    }
  },
  methods: {
    ...mapActions('projects', ['fetchProjectById']), // agar bunday action bo'lsa
    async loadProject() {
      // Loyihani o'zingiz yozgan fetchProjectById action orqali oling,
      // yoki to'g'ridan-to'g'ri axios orqali `/api/projects/${id}/`
      const response = await this.$store.dispatch('projects/fetchProjectById', this.projectId)
      this.project = response
    }
  },
  created() {
    this.loadProject()
  }
}
</script>
