# 📦 Процесс: Обработка заявки (`Process_request`)

## 🧑‍💼 Участник: `Operator`

---

## 🔹 Service Tasks

### 🔧 `Activity_lead_exist` — Поиск лида
**Тип задачи:** `lead_exists`  
**Получает:**
- `phone: string`  
**Возвращает:**
- `is_lead_exists: boolean`

---

### 🆕 `Activity_lead_create` — Создание лида  
**Тип задачи:** `lead_create`  
**Получает:**
- `phone: string`  
**Возвращает:**
- `lead: object`

---

## 🔹 User Tasks

### 📝 `Activity_lead_info` — Обработка лида  
**Форма:** `form-lead-processing`  
**Возвращает:**
- `lead_info: string`
- `is_task_need: boolean`

---

### ⚙️ `Activity_task_options` — Опции заказа  
**Форма:** `Form_hy1x5cl`  
**Возвращает:**
- `task_options: list`

---

### ❌ `Activity_refuse` — Оформить отказ  
**Форма:** `form-1nt4n0x`  
**Возвращает:**
- `draw_refuse: string`

---

## 🔹 Gateways

### 🔀 `Gateway_is_lead_exists` — Лид найден?  
- Да → переход к `lead_info`
- Нет (`is_lead_exists=false`) → `lead_create`

---

### 🔀 `Gateway_result_task` — Задача требуется?  
- Да → `task_options`
- Нет (`is_task_need=false`) → `refuse`

---

## 🔹 End Events

### ✅ `Event_complete` — Заявка обработана  
Завершает процесс, если заказ оформлен.

---

### 🟥 `Event_refuse` — Отказ  
Terminate Event при отказе от заявки.

---

## 🗺️ Общий сценарий

1. **Start Event** — `Обработка заявки`
2. **Service Task** — Проверка наличия лида (`lead_exists`)
3. **Gateway** — Лид найден?
   - Если нет — Создание лида (`lead_create`)
4. **User Task** — Обработка лида (`lead_info`)
5. **Gateway** — Требуется задача?
   - Да → `task_options` → `Event_complete`
   - Нет → `refuse` → `Event_refuse`

---

## 📝 Комментарии

- Используются Service Task с `zeebe:taskDefinition`, все user tasks сопровождаются `zeebe:formDefinition`.
- Потоки правильно используют условия `=is_lead_exists=false`, `=is_task_need=false`.
- `terminateEvent` оформлен корректно для завершения по отказу.
- Названия событий и задач соответствуют назначению.