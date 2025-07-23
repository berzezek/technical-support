# SaintSir BPMN service

---

## 🧩 Main Process: `Process_main`

### 🔁 Task Flow
**Обработка → Забор → Поступление → Диагностика → Согласование → Ремонт → Передача → Доставка (или Самовывоз)**  
**Operator → Pick → Inbound → Diagnostics → Coordination → Repair → Outbound → Delivery/Self-pick**

---

### 🚀 Start Event
- **Start:** `Начало процесса`

---

### 🔹 Call Activities

#### 📦 `Activity_request` — Обработка
- Вызов процесса: `Process_request`

#### 🚚 `Activity_pick` — Забор
- Вызов процесса: `Process_pick`

#### 📥 `Activity_inbound` — Поступление
- Вызов процесса: `Process_inbound`

#### 🧪 `Activity_diagnostics` — Диагностика
- Вызов процесса: `Process_diagnostics`

#### 🧾 `Activity_coordination` — Согласование
- Вызов процесса: `Process_coordination`

#### 🛠️ `Activity_repair` — Ремонт
- Вызов процесса: `Process_repair`

#### 🔁 `Activity_outbound` — Передача
- Вызов процесса: `Process_outbound`

#### 🚛 `Activity_delivery` — Доставка
- Вызов процесса: `Process_delivery`

---

### 🔀 Gateways

#### `Gateway_1kefjik` — Способ доставки до сервиса
- Условие: `task_option[1] = "self_delivery"`
- Варианты:
  - Самодоставка → `Activity_inbound`
  - Курьер → `Activity_pick`

#### `Gateway_0okztn9` — Способ получения клиентом
- Условие: `task_options[2] = "self_pick"`
- Варианты:
  - Самовывоз → `Event_task_process_success`
  - Доставка → `Activity_delivery`

---

### 🏁 End Event
- **Успех:** `Event_task_process_success`

---

### 📝 Примечания
- Все CallActivity используют `propagateAllChildVariables=false`
- Используются условные переходы на основе массива `task_options`
- Процесс включает два основных шлюза: для направления техники в сервис и клиенту после ремонта

---

## 🔧 Переменные

### Входные:
- `phone: string`

### Внутренние:
- `task_option: list[string]` — используется для маршрутизации внутри процесса

---

## 🧠 Подпроцессы (используемые):
- `Process_request`
- `Process_pick`
- `Process_inbound`
- `Process_diagnostics`
- `Process_coordination`
- `Process_repair`
- `Process_outbound`
- `Process_delivery`