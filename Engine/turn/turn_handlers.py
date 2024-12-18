from Entities.Warlord.warlord import Warlord


def end_turn(active_warlord: Warlord):
    for squad in active_warlord.squads:
        squad.reset_speed()

    print(f"{str(active_warlord)} turn ended!")
