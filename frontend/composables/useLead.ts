export interface LeadContext {
  leads: Ref<Lead[]>;
  lead: Ref<Lead | null>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  fetchLeads: () => Promise<void>;
  fetchLeadsByPhone: (phone: string) => Promise<void>;
  fetchLeadById: (id: number) => Promise<void>;
  createLead: (lead: Partial<Lead>) => Promise<void>;
  updateLead: (id: number, lead: Partial<Lead>) => Promise<void>;
  deleteLead: (id: number) => Promise<void>;
}

export interface Lead {
  id: number;
  created_at: string;
  updated_at: string;
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  description?: string | null;
}



export const useLead = (): LeadContext => {
  const leads = ref<Lead[]>([]);
  const lead = ref<Lead | null>(null);
  const loading = ref<boolean>(false);
  const error = ref<string | null>(null);

  const config = useRuntimeConfig();
  const token = useCookie('auth_token');

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  };

  async function fetchLeads(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Lead[]>('/api/v1/leads', {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Leads] Получены лиды:', response);
      leads.value = response;
    } catch (err) {
      error.value = 'Ошибка при загрузке лидов';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchLeadsByPhone(phone: string): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Lead[]>(`/api/v1/leads/search-leads-by-phone?phone=${phone}`, {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      leads.value = response;
    } catch (err) {
      error.value = 'Ошибка при поиске по телефону';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchLeadById(id: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const result = await $fetch<Lead>(`/api/v1/leads/${id}`, {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      lead.value = result;
    } catch (err) {
      error.value = 'Ошибка при получении лида';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function createLead(newLead: Partial<Lead>): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const created = await $fetch<Lead>('/api/v1/leads', {
        baseURL: config.public.apiBaseUrl,
        method: 'POST',
        body: newLead,
        ...authHeaders,
      });
      leads.value.push(created);
    } catch (err) {
      error.value = 'Ошибка при создании лида';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function updateLead(id: number, updatedLead: Partial<Lead>): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const updated = await $fetch<Lead>(`/api/v1/leads/${id}`, {
        baseURL: config.public.apiBaseUrl,
        method: 'PUT',
        body: updatedLead,
        ...authHeaders,
      });
      const index = leads.value.findIndex((l) => l.id === id);
      if (index !== -1) leads.value[index] = updated;
    } catch (err) {
      error.value = 'Ошибка при обновлении лида';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function deleteLead(id: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      await $fetch(`/api/v1/leads/${id}`, {
        baseURL: config.public.apiBaseUrl,
        method: 'DELETE',
        ...authHeaders,
      });
      leads.value = leads.value.filter((l) => l.id !== id);
    } catch (err) {
      error.value = 'Ошибка при удалении лида';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  return {
    leads,
    lead,
    loading,
    error,
    fetchLeads,
    fetchLeadsByPhone,
    fetchLeadById,
    createLead,
    updateLead,
    deleteLead,
  };
};
