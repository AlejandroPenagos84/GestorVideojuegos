import { manager_tournaments_api } from "@/api/managementApi"
import type { Tournament } from "../interfaces/tournament.interface"

export const getTournamentsAction = async ()=>{
    try{
        const {data} = await manager_tournaments_api.get<Tournament[]>('/tournaments')
        console.log(data)
        return data
    }catch(error){
        console.log(error)
        throw new Error('Error getting tournaments')
    }
}