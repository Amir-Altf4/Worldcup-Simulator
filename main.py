# =======================
# دانشجو: امیرمحمد باقری
# 404130433 : شماره دانشجویی
# عنوان پروژه: شبیه ساز جام جهانی
# تاریخ تحویل: 1405/5/3
# =======================

from modules.worldcup_simulator import WorldCupSimulator

# اجرای برنامه فقط در صورتی که این فایل مستقیماً اجرا شود
if __name__ == "__main__":
    
    # ساخت شیء اصلی شبیه‌ساز
    simulator = WorldCupSimulator()
    
    # نمایش منو تا زمانی که کاربر گزینه خروج را انتخاب کند
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
        
        # بارگذاری اطلاعات تیم‌ها از فایل
        if choice == "1":
            simulator.load_teams_from_csv("worldcup_2026_teams.txt")
            print(f"✅ {len(simulator.teams)} Team loaded")
    
        # انجام سیدبندی و قرعه‌کشی گروه‌ها
        elif choice == "2":
            if not simulator.teams:
                print("Load teams first")
            else:
                simulator.seed_and_draw()
                
        # اجرای مرحله گروهی و نمایش جدول گروه‌ها
        elif choice == "3":
            if not simulator.groups:
                print("Do seed & draw first")
            else:
                simulator.run_group_stage()
                
        # اجرای کامل مسابقات و نمایش قهرمان
        elif choice == "4":
            if not simulator.teams:
                print("Load teams first") 
            else:
                simulator.run_full_simulation()
                
        # اجرای چندباره شبیه‌سازی و محاسبه درصد قهرمانی تیم‌ها
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
                    
        # نمایش براکت مرحله حذفی آخرین شبیه‌سازی
        elif choice == "6":
            if not simulator.champion:
                print("Do a simulation first")
            else:
                simulator.display_bracket()
                
        elif choice == "7":
            print("exit")
            break
        
        # مدیریت ورودی‌های نامعتبر
        else:
            print("invalid choice! please try again.")