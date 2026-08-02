from modules.worldcup_simulator import WorldCupSimulator

# Run the program only if this file is executed directly
if __name__ == "__main__":
    
    # Create the main simulator object
    simulator = WorldCupSimulator()
    
    # Show the menu until the user chooses to exit
    while True:
        print("=== WorldCup Simulator ===")
        print("1. Loading teams from CSV")
        print("2. Doing seed & draw")
        print("3. Run the group stage and display each group's standings")
        print("4. Run the full tournament (group stage + knockout) and display the champion")
        print("5. Simulate the tournament 1,000 times and report championship percentages")
        print("6. Display the knockout bracket from the last simulation")
        print("7. Exit")
    
        choice = input("Choose: ")
        
        # Load teams data from file
        if choice == "1":
            simulator.load_teams_from_csv("worldcup_2026_teams.txt")
            print(f"✅ {len(simulator.teams)} Team loaded")
    
        # Perform seeding and drawing of groups
        elif choice == "2":
            if not simulator.teams:
                print("Load teams first")
            else:
                simulator.seed_and_draw()
                
        # Run the group stage and display each group's table
        elif choice == "3":
            if not simulator.groups:
                print("Do seed & draw first")
            else:
                simulator.run_group_stage()
                
        # Run the full tournament and display the champion
        elif choice == "4":
            if not simulator.teams:
                print("Load teams first") 
            else:
                simulator.run_full_simulation()
                
        # Run multiple simulations and calculate championship percentages
        elif choice == "5":
            if not simulator.teams:
                print("Load teams first")
            else:            
                num_simulation = int(input("enter the number of simulations: "))
                if num_simulation <= 0:
                    print("Number should be greater than 0")
                else:
                    champions = simulator.most_likely_champion(int(num_simulation))
                    simulator.plot_champion_stats(champions, num_simulation)
                    
        # Display the knockout bracket from the last simulation
        elif choice == "6":
            if not simulator.champion:
                print("Do a simulation first")
            else:
                simulator.display_bracket()
                
        elif choice == "7":
            print("exit")
            break
        
        # Handle invalid inputs
        else:
            print("invalid choice! please try again.")