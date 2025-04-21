using System;
using System.Threading;

class BitShiftAnimation
{
    static void Main()
    {
        Console.Clear();
        Console.CursorVisible = false;
        

        int number = 0b_0000_1111;
        int bits = 8;
        int shiftSteps = 5;
        bool shiftLeft = true;


        Console.WriteLine("Исходное число:");
        PrintBinary(number, bits);
        Thread.Sleep(1000);


        for (int i = 0; i < shiftSteps; i++)
        {
            Console.SetCursorPosition(0, Console.CursorTop - 1);
            Console.WriteLine(new string(' ', Console.WindowWidth));
            Console.SetCursorPosition(0, Console.CursorTop - 1);

            number = shiftLeft ? number << 1 : number >> 1;
            PrintBinaryWithAnimation(number, bits, shiftLeft);
            Thread.Sleep(500);
        }

        Console.CursorVisible = true;
    }

    static void PrintBinary(int number, int bits)
    {
        Console.Write("[");
        for (int i = bits - 1; i >= 0; i--)
        {
            Console.Write((number & (1 << i)) != 0 ? "1" : "0");
            if (i % 4 == 0 && i != 0) Console.Write(" ");
        }
        Console.WriteLine("]\n");
    }

    static void PrintBinaryWithAnimation(int number, int bits, bool shiftLeft)
    {
        Console.Write("[");
        for (int i = bits - 1; i >= 0; i--)
        {
            var color = (i == (shiftLeft ? bits - 1 : 0)) ? 
                ConsoleColor.Red : ConsoleColor.White;
            
            Console.ForegroundColor = color;
            Console.Write((number & (1 << i)) != 0 ? "1" : "0");
            Console.ResetColor();
            
            if (i % 4 == 0 && i != 0) Console.Write(" ");
        }
        Console.WriteLine("]");
        Console.WriteLine(shiftLeft ? 
            "▲ Сдвиг влево      " : 
            "▼ Сдвиг вправо     ");
    }
}