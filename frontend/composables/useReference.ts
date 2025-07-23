export interface Category {
  id: number;
  name: string;
  description?: string | null;
}

export interface Product {
  id: number;
  name: string;
  description?: string | null;
  category_id: number;
  category?: Category | null;
}

export const useReference = () => {
  const categories = ref<Category[]>([]);
  const category = ref<Category | null>(null);
  const product = ref<Product | null>(null);
  const products = ref<Product[]>([]);
  const loading = ref<boolean>(false);
  const error = ref<string | null>(null);

  const config = useRuntimeConfig();
  const token = useCookie('auth_token');

  const authHeaders = {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  };

  async function fetchCategories(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Category[]>('/api/v1/categories', {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Categories] Получены категории:', response);
      categories.value = response;
    } catch (err) {
      error.value = 'Ошибка при загрузке категорий';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchProducts(): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Product[]>('/api/v1/products', {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Products] Получены продукты:', response);
      products.value = response;
    } catch (err) {
      error.value = 'Ошибка при загрузке продуктов';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchCategoryById(id: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Category>(`/api/v1/categories/${id}`, {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Category] Получена категория:', response);
      category.value = response;
    } catch (err) {
      error.value = 'Ошибка при загрузке категории';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchProductById(id: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Product>(`/api/v1/products/${id}`, {
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Product] Получен продукт:', response);
      product.value = response;
    } catch (err) {
      error.value = 'Ошибка при загрузке продукта';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function patchCategory(
    id: number,
    data: Partial<Category>
  ): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Category>(`/api/v1/categories/${id}`, {
        method: 'PATCH',
        body: data,
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Category] Обновлена категория:', response);
      category.value = response;
    } catch (err) {
      error.value = 'Ошибка при обновлении категории';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function patchProduct(
    id: number,
    data: Partial<Product>
  ): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      const response = await $fetch<Product>(`/api/v1/products/${id}`, {
        method: 'PATCH',
        body: data,
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Product] Обновлен продукт:', response);
      product.value = response;
    } catch (err) {
      error.value = 'Ошибка при обновлении продукта';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function deleteCategory(id: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      await $fetch(`/api/v1/categories/${id}`, {
        method: 'DELETE',
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Category] Категория удалена:', id);
      categories.value = categories.value.filter((cat) => cat.id !== id);
      category.value = null;
    } catch (err) {
      error.value = 'Ошибка при удалении категории';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  async function deleteProduct(id: number): Promise<void> {
    loading.value = true;
    error.value = null;
    try {
      await $fetch(`/api/v1/products/${id}`, {
        method: 'DELETE',
        baseURL: config.public.apiBaseUrl,
        ...authHeaders,
      });
      console.log('[Product] Продукт удален:', id);
      products.value = products.value.filter((prod) => prod.id !== id);
      product.value = null;
    } catch (err) {
      error.value = 'Ошибка при удалении продукта';
      console.error(error.value, err);
    } finally {
      loading.value = false;
    }
  }

  return {
    categories,
    category,
    product,
    products,
    loading,
    error,
    fetchCategories,
    fetchProducts,
    fetchCategoryById,
    fetchProductById,
    patchCategory,
    patchProduct,
    deleteCategory,
    deleteProduct,
  };
};
