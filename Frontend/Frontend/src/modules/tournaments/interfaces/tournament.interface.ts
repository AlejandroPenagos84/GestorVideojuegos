export interface Tournament {
    uid_tournament:          string;
    name:                    string;
    description:             string;
    type:                    string;
    start_date:              Date;
    end_date:                Date;
    minimun_player_per_team: number;
    minimun_player_general:  number;
}
