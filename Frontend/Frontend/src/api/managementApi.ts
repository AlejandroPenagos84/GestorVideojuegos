import axios from 'axios'

const manager_tournaments_api = axios.create(
    {
        baseURL: import.meta.env.VITE_MANAGE_TOURNAMENTS_API
    }
)

console.log(import.meta.env)
export {manager_tournaments_api}