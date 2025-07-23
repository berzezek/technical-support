export interface Task {
  id: number;
  lead_id: number;
  user_id: string;
  title: string;
  description?: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface TaskContext {
  tasks: Ref<Task[]>;
  task: Ref<Task | null>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  fetchTasks: (leadId: number) => Promise<void>;
  fetchTask: (leadId: number, taskId: number) => Promise<void>;
  createTask: (leadId: number, task: TaskCreate) => Promise<void>;
  updateTask: (
    leadId: number,
    taskId: number,
    task: TaskUpdate
  ) => Promise<void>;
  deleteTask: (leadId: number, taskId: number) => Promise<void>;
  completeTask: (leadId: number, taskId: number) => Promise<void>;
  reopenTask: (leadId: number, taskId: number) => Promise<void>;
}

export const useTask = (): TaskContext => {
  const tasks = ref<Task[]>([]);
  const task = ref<Task | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const config = useRuntimeConfig();
  const token = useCookie('auth_token');

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  };

  async function fetchTasks(leadId: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const res = await $fetch<TaskListResponse>(`/leads/${leadId}/tasks`, {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      tasks.value = res.tasks;
    } catch (err) {
      error.value = 'Ошибка при загрузке задач';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchTask(leadId: number, taskId: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const res = await $fetch<Task>(`/leads/${leadId}/tasks/${taskId}`, {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      task.value = res;
    } catch (err) {
      error.value = 'Ошибка при загрузке задачи';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function createTask(
    leadId: number,
    taskData: TaskCreate
  ): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const newTask = await $fetch<Task>(`/leads/${leadId}/tasks`, {
        baseURL: config.public.apiBaseUrl,
        method: 'POST',
        body: taskData,
        ...authHeaders,
      });
      tasks.value.push(newTask);
    } catch (err) {
      error.value = 'Ошибка при создании задачи';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function updateTask(
    leadId: number,
    taskId: number,
    taskData: TaskUpdate
  ): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const updated = await $fetch<Task>(`/leads/${leadId}/tasks/${taskId}`, {
        baseURL: config.public.apiBaseUrl,
        method: 'PATCH',
        body: taskData,
        ...authHeaders,
      });
      const index = tasks.value.findIndex((t) => t.id === taskId);
      if (index !== -1) tasks.value[index] = updated;
    } catch (err) {
      error.value = 'Ошибка при обновлении задачи';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function deleteTask(leadId: number, taskId: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      await $fetch(`/leads/${leadId}/tasks/${taskId}`, {
        baseURL: config.public.apiBaseUrl,
        method: 'DELETE',
        ...authHeaders,
      });
      tasks.value = tasks.value.filter((t) => t.id !== taskId);
    } catch (err) {
      error.value = 'Ошибка при удалении задачи';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function completeTask(leadId: number, taskId: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const res = await $fetch<Task>(
        `/leads/${leadId}/tasks/${taskId}/complete`,
        {
          baseURL: config.public.apiBaseUrl,
          method: 'POST',
          ...authHeaders,
        }
      );
      const index = tasks.value.findIndex((t) => t.id === taskId);
      if (index !== -1) tasks.value[index] = res;
    } catch (err) {
      error.value = 'Ошибка при завершении задачи';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function reopenTask(leadId: number, taskId: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const res = await $fetch<Task>(
        `/leads/${leadId}/tasks/${taskId}/reopen`,
        {
          baseURL: config.public.apiBaseUrl,
          method: 'POST',
          ...authHeaders,
        }
      );
      const index = tasks.value.findIndex((t) => t.id === taskId);
      if (index !== -1) tasks.value[index] = res;
    } catch (err) {
      error.value = 'Ошибка при переоткрытии задачи';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  return {
    tasks,
    task,
    loading,
    error,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask,
    completeTask,
    reopenTask,
  };
};
