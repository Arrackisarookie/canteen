<script setup>
import { reactive } from 'vue'
import { ref, computed, onMounted, watch } from 'vue'

const counter = reactive({ count: 0 })
const message = ref('Hello World!')
const titleClass = ref('title')
const text = ref('')
const awesome = ref(true)

function increase() {
  counter.count ++
}

function toggle() {
  awesome.value = !awesome.value
}

let id = 0
const hideCompleted = ref(false)
const newTodo = ref('')
const todos = ref([
  { id: id++, text: 'Learn HTML', done: false},
  { id: id++, text: 'Learn CSS', done: false},
  { id: id++, text: 'Learn JavaScript', done: false}
])
const filteredTodos = computed(() => {
  return hideCompleted.value
    ? todos.value.filter((t) => !t.done)
    : todos.value
})

function addTodo() {
  todos.value.push({id: id++, text: newTodo.value, done: false})
  newTodo.value = ''
}

function removeTodo(todo) {
  todos.value = todos.value.filter((t) => t != todo)
}

const pElementRef = ref(null)
onMounted(() => {
  pElementRef.value.textContent = 'mounted'
})

const todoId = ref(1)
const todoData = ref(null)

async function fetchData() {
  todoData.value = null
  const res = await fetch(
    `https://jsonplaceholder.typicode.com/todos/${todoId.value}`
  )
  todoData.value = await res.json()
}

fetchData()

watch(todoId, fetchData)
</script>

<template>
  <h1 :class="titleClass">{{ message.split('').reverse().join('') }}</h1>
  <button @click="increase">Count is: {{ counter.count }}</button>
  <input v-model="text">
  <p>{{ text }}</p>

  <button @click="toggle">toggle</button>
  <h1 v-if="awesome">Vue is awesome!</h1>
  <h1 v-else>Oh no 😢</h1>

  <form @submit.prevent="addTodo">
    <input v-model="newTodo" required placeholder="New Todo">
    <button>Add Todo</button>
  </form>
  <ul>
    <li v-for="todo in filteredTodos" :key="todo.id">
      <input type="checkbox" v-model="todo.done">
      <span :class="{ done: todo.done }">{{ todo.text }}</span>
      <button @click="removeTodo(todo)">x</button>
    </li>
  </ul>
  <button @click="hideCompleted = !hideCompleted">
    {{ hideCompleted ? 'Show All' : 'Hide Completed' }}
  </button>
  <p ref="pElementRef">Hello</p>

  <p>Todo id: {{ todoId }}</p>
  <button @click="todoId++" :disabled="!todoData">Fetch next todo</button>
  <p v-if="!todoData">Loading...</p>
  <pre v-else>{{ todoData }}</pre>
</template>

<style>
.title {
  color: red;
}
.done {
  text-decoration: line-through;
}
</style>
