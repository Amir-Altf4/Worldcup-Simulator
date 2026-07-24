import random
from match import Match

class Group:
    """نماینده یک گروه در مرحله گروهی جام جهانی.

    این کلاس تیم‌های یک گروه را مدیریت می‌کند، مسابقات دوره‌ای
    گروه را برگزار می‌کند و رتبه‌بندی را محاسبه می‌کند.
    """

    def __init__(self, name, teams):
        """یک گروه جدید با نام و لیست تیم‌ها ایجاد می‌کند.

        Args:
            name (str): نام گروه (مثلاً «A»).
            teams (list[Team]): لیست تیم‌های عضو این گروه.
        """
        self.name = name
        self.teams = teams
        
    def play_all_matches(self):
        """تمام مسابقات دوره‌ای بین تیم‌های گروه را برگزار می‌کند.

        هر تیم یک بار در برابر هر تیم دیگر گروه بازی می‌کند.

        Returns:
            None
        """
        
        # پیمایش تمام تیم‌های گروه
        for i in range(len(self.teams)):
            # j از i+1 شروع می‌شود تا از تکرار بازی‌ها جلوگیری شود
            for j in range(i + 1, len(self.teams)):
                
                # ایجاد مسابقه بین دو تیم
                match = Match(self.teams[i], self.teams[j])
                match.play()
    
    def get_ranking(self):
        """تیم‌های گروه را بر اساس امتیاز و معیارهای tie-break مرتب می‌کند.

        معیارهای رتبه‌بندی به ترتیب: امتیاز، تفاضل گل، گل زده
        و در صورت تساوی کامل، انتخاب تصادفی.

        Returns:
            list[Team]: لیست تیم‌ها به ترتیب نزولی رتبه.
        """
        
        # مرتب‌سازی تیم‌ها بر اساس معیارهای رتبه‌بندی
        self.teams.sort(
        key = lambda t: (t.points, t.goal_difference(), t.goals_for, random.random()),
        reverse = True    
        )
        # بازگرداندن جدول نهایی گروه
        return self.teams
    
    def advance_teams(self):
        """دو تیم برتر گروه را برای مرحله حذفی برمی‌گرداند.

        Returns:
            list[Team]: دو تیم اول جدول رتبه‌بندی گروه.
        """
        
        # دریافت جدول رتبه‌بندی
        ranking = self.get_ranking()
        
        # بازگرداندن دو تیم برتر
        return ranking[:2]