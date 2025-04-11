using System;
using System.Runtime.Intrinsics.X86;

public class bMoney
{
    private decimal amount;

    public bMoney(decimal amount)
    {
        this.amount = amount;
    }

    public static explicit operator bMoney(double d)
    {
        return new bMoney((decimal)d);
    }

    public static bMoney operator +(bMoney a, bMoney b)
    {
        return new bMoney(a.amount + b.amount);
    }

    public static bMoney operator -(bMoney a, bMoney b)
    {
        return new bMoney(a.amount - b.amount);
    }

    public static bMoney operator *(bMoney money, double multiplier)
    {
        return new bMoney(money.amount * (decimal)multiplier);
    }

    public static double operator /(bMoney a, bMoney b)
    {
        return (double)(a.amount / b.amount);
    }

    public static bMoney operator /(bMoney money, int divisor)
    {
        return new bMoney(money.amount / divisor);
    }

    public override string ToString()
    {
        return this.amount.ToString();
    }
}

class Program
{
    static void Main()
    {
        while (true)
        {
            try
            {
                Console.WriteLine("Первые шекеля (например $1,234.56):");
                bMoney m1 = new bMoney(Convert.ToDecimal(Console.ReadLine()));

                Console.WriteLine("Вторые шекеля:");
                bMoney m2 = new bMoney(Convert.ToDecimal(Console.ReadLine()));

                Console.WriteLine("Цифра для операций:");
                double d = double.Parse(Console.ReadLine() ?? "1");
                int n = (int)d;

                bMoney sum = m1 + m2;
                bMoney difference = m1 - m2;
                bMoney product = m1 * d;
                double quotient = m1 / m2;
                bMoney divisionByInt = m1 / n;

                Console.WriteLine($"Сумма: {sum}");
                Console.WriteLine($"Разница: {difference}");
                Console.WriteLine($"Умножение: {product}");
                Console.WriteLine($"Деление: {quotient:F2}");
                Console.WriteLine($"Деление на цифру: {divisionByInt}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ошибка: {ex.Message}");
            }

            Console.WriteLine("Продолжить? (y/n)");
            if ((Console.ReadLine() ?? "y").Trim().ToLower() != "y")
                break;
        }
    }
}