// composables/useTasksSocket.ts
import { ref } from 'vue';

const socket = ref<WebSocket | null>(null);
const process_instances = ref<any[]>([]);
const process_definitions = ref<any[]>([]);
const messages = ref<string[]>([]);

let reconnecting = false;
let reconnectAttempts = 0;

export const useTasksSocket = () => {
  const config = useRuntimeConfig();

  const WEBSOCKET_BASE_URL =
    config.public.websocketBaseUrl || 'ws://localhost:8000';

  const connect = async () => {
    console.log('[WebSocket] Подключение к серверу...');
    if (socket.value || reconnecting) return;

    const wsUrl = `${WEBSOCKET_BASE_URL}/bpmn/ws/tasks?user_id=123&group=Operator`;
    console.log('[WebSocket] Подключение к', wsUrl);

    reconnecting = true;
    socket.value = new WebSocket(wsUrl);

    socket.value.onopen = () => {
      console.log('[WebSocket] ✅ Соединение открыто');
      reconnecting = false;
      reconnectAttempts = 0;
    };

    socket.value.onmessage = (event) => {
      console.log('[WebSocket] 📥 Получено:', event.data);
      messages.value.push(event.data);

      try {
        const parsed = JSON.parse(event.data);

        if (parsed?.type === 'process_definitions') {
          process_definitions.value = parsed.data?.items || [];
          console.log('[WebSocket] 📘 Обновлены определения процессов:', process_definitions.value);
        }

        if (parsed?.type === 'process_instances') {
          process_instances.value = parsed.data?.items || [];
          console.log('[WebSocket] 🔁 Обновлены экземпляры процессов:', process_instances.value);
        }

      } catch (e) {
        console.warn('[WebSocket] ⚠️ Ошибка парсинга:', e);
      }
    };

    socket.value.onerror = async (err) => {
      console.error('[WebSocket] ❌ Ошибка:', err);
      socket.value?.close();
      socket.value = null;

      reconnectAttempts++;
      if (reconnectAttempts > 5) {
        console.warn('[WebSocket] 🚫 Слишком много попыток переподключения');
        return;
      }
    };

    socket.value.onclose = (event) => {
      console.warn(
        '[WebSocket] 🔌 Соединение закрыто:',
        event.code,
        event.reason
      );
      socket.value = null;
    };
  };

  const disconnect = () => {
    if (socket.value) {
      console.log('[WebSocket] ❎ Отключение');
      socket.value.close();
      socket.value = null;
    }
  };

  return {
    connect,
    disconnect,
    process_instances,
    process_definitions,
    messages,
  };
};
