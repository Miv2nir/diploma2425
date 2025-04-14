import { mount } from 'svelte'
import '../../backend/static/style.css'
import App from './App.svelte'

const app = mount(App, {
  //target: document.getElementById('app'),
  target: document.body,
})

export default app
