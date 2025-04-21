using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace v3
{
    public class Time
    {
        private int hr, mn, sc;
        public Time()
        {
            hr = 0;
            mn = 0;
            sc = 0;
        }
        public Time(int h, int m, int s)
        {
            hr = h;
            mn = m;
            sc = s;
            NormalizeTime();
        }

        private void NormalizeTime()
        {
            mn += sc / 60;
            sc %= 60;
            hr += mn / 60;
            mn %= 60;
            hr %= 24;
        }

        public static Time operator +(Time t1, Time t2)
        {
            int totalHr = t1.hr + t2.hr;
            int totalMn = t1.mn + t2.mn;
            int totalSc = t1.sc + t2.sc;
            return new Time(totalHr, totalMn, totalSc);
        }

        public override string ToString()
        {
            return $"{hr:D2}:{mn:D2}:{sc:D2}";
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Time t1 = new Time(10, 30, 45);
            Time t2 = new Time(5, 45, 20);

            Time t3 = t1 + t2;

            Console.WriteLine($"Время 1: {t1}");
            Console.WriteLine($"Время 2: {t2}");
            Console.WriteLine($"Время 1 + Время 2: {t3}");

            // Проверка переполнения
            Time t4 = new Time(23, 59, 59);
            Time t5 = new Time(0, 0, 1);
            Time t6 = t4 + t5;

            Console.WriteLine($"\nВремя 4: {t4}");
            Console.WriteLine($"Время 5: {t5}");
            Console.WriteLine($"Время 4 + Время 5: {t6}"); // Должно быть 00:00:00
        }
    }
}