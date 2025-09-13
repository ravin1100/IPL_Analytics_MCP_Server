from fastmcp import FastMCP

from agent import process_query

mcp = FastMCP("IPL Analytics MCP Server")


@mcp.tool
def query_player_stats(player_name: str, stat_type: str) -> str:
    """
    Fetch player statistics based on the player's name and the type of statistic requested.
    stat_type can be one of: 'batting', 'bowling', 'fielding', 'all-round'
    player_name: Full name of the player (e.g., "Virat Kohli")
    stat_type: Type of statistics to retrieve (e.g., "batting")
    """

    instruction_prompt = f"""
    Fetch player statistics based on the player's name and the type of statistic requested.
    stat_type can be one of: 'batting', 'bowling', 'fielding', 'all-round'
    player_name: Full name of the player (e.g., "Virat Kohli")
    stat_type: Type of statistics to retrieve (e.g., "batting")

    player_name: {player_name}
    stat_type: {stat_type}
    """
    return process_query(user_query=instruction_prompt)


@mcp.tool
def match_analysis(match_id: str) -> str:
    """
    Provide detailed analysis of a specific match given its unique identifier.
    match_id: Unique identifier for the match (e.g., "2023-IPL-01")

    """

    instruction_prompt = f"""
    Provide detailed analysis of a specific match given its unique identifier.  
    match_id: {match_id}
    """
    return process_query(user_query=instruction_prompt)


@mcp.tool
def team_performance(team_name: str, season: str) -> str:
    """
    Analyze the performance of a specific team during a given season.
    season: Year of the season (e.g., "2023")
    team_name: Full name of the team (e.g., "Mumbai Indians")
    """

    instruction_prompt = f"""
    Analyze the performance of a specific team during a given season.
    team_name: {team_name}
    season: {season}
    """
    return process_query(user_query=instruction_prompt)


@mcp.tool
def season_comparisons(season1: str, season2: str) -> str:
    """
    Compare two different seasons in terms of overall statistics, team performances, and player achievements.
    season1 and season2: Years of the seasons to compare (e.g., "2022", "2023")

    """

    instruction_prompt = f"""
    Compare two different seasons in terms of overall statistics, team performances, and player achievements.
    season1: {season1}
    season2: {season2}
    """
    return process_query(user_query=instruction_prompt)


@mcp.tool
def head_to_head(team1: str, team2: str) -> str:
    """
    Provide historical data and statistics for matches played between two teams.
    team1 and team2: Full names of the teams (e.g., "Chennai Super Kings", "Royal Challengers Bangalore")

    """

    instruction_prompt = f"""
    Provide historical data and statistics for matches played between two teams.
    team1: {team1}
    team2: {team2}
    """
    return process_query(user_query=instruction_prompt)


if __name__ == "__main__":
    mcp.run()
