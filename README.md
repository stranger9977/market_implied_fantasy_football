# Catchy Name Here: Fantasy Football Forecasting App

## Overview
This is a full-stack web application designed to forecast fantasy football outcomes using Vegas sportsbook odds data. The application provides data-driven, validated projections, waiver wire recommendations, and optimal DFS lineups. It aims to help users increase their success rate in various types of fantasy football contest formats, streamlining the process with a focus on data science best practices.

## Features
- **Projections:** Generates player projections based on Vegas sportsbook odds.
- **Waiver Wire:** Recommends top pickups and drops.
- **Lineup Setter:** Helps users set their optimal lineup.
- **DFS Lineup Generator:** Generates optimal lineups for various DFS contests.
- **Grading Module:** Evaluates the recommendations based on data science best practices.

## Future Plans
- Transition from a Python notebook to a full-stack web application.
- Implement a subscription-based model to monetize the platform.
- Add additional features based on user feedback and market demands.

## Technologies Used
- Python
- Machine Learning Libraries (e.g., scikit-learn, TensorFlow)
- SQL (for data manipulation and queries)
- [Future: Web Development Stack]

## To-Do List for APP
### General
#### Data Storage & Workflow
- [✅] Automate the storage of the data.
- [✅] Ensure GitHub Action workflow works as intended. - Updates each day at 11EST and also can be done manually.
#### Data Fetching
- [ ] Learn [nektos/act](https://github.com/nektos/act) for testing purposes.
- [ ] Add more sources to the fetch_data.py file.
- [ ] Write tests for new data sources.
#### Data Processing
- [ ] Finish the dataprocess.py file.
- [ ] Complete the utils file.
- [ ] Implement a local machine workflow that complements the GitHub Actions.
- [ ] Complete data transformation steps.
#### DFS Lineup Generator
- [ ] Structure data for DFS optimizer.
- [ ] Implement DFS optimizer to generate up to 5000 lineups.
- [ ] Incorporate ownership projections.
#### Start/Sit/Waivers Tool
- [ ] Sync with Sleeper leagues (and eventually other platforms).
- [ ] Design a user-friendly interface.
#### Waiver Wire Tool
- [ ] Implement top pickups and drops recommendations.
- [ ] Suggest bid amounts based on the makeup of the user's team.
#### Project Structure
- [ ] Make sure project structure aligns with Streamlit's 2023 documentation.
- [ ] If possible, incorporate historical odds (low priority).

