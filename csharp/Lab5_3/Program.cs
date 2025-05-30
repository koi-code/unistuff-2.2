using System;

abstract class Data
{
    public abstract void Display();
    public abstract void Save();
    public abstract void Process();
}

class SignalData : Data
{
    private double[] signalValues;
    
    public SignalData(double[] values)
    {
        signalValues = values;
    }
    
    public override void Display()
    {
        Console.WriteLine("Отображение сигнала:");
        foreach (var value in signalValues)
        {
            Console.Write(value + " ");
        }
        Console.WriteLine();
    }
    
    public override void Save()
    {
        Console.WriteLine($"Сохранение {signalValues.Length} значений сигнала в базу данных");
    }
    
    public override void Process()
    {
        Console.WriteLine("Обработка сигнала: фильтрация и анализ");
    }
}

class ProcessedResultData : Data
{
    private string analysisResult;
    
    public ProcessedResultData(string result)
    {
        analysisResult = result;
    }
    
    public override void Display()
    {
        Console.WriteLine($"Отображение результатов: {analysisResult}");
    }
    
    public override void Save()
    {
        Console.WriteLine("Сохранение результатов обработки в отчет");
    }
    
    public override void Process()
    {
        Console.WriteLine("Дополнительная обработка результатов: статистический анализ");
    }
}

class AuxiliaryData : Data
{
    private string metadata;
    
    public AuxiliaryData(string meta)
    {
        metadata = meta;
    }
    
    public override void Display()
    {
        Console.WriteLine($"Отображение метаданных: {metadata}");
    }
    
    public override void Save()
    {
        Console.WriteLine("Сохранение вспомогательных данных в конфигурационный файл");
    }
    
    public override void Process()
    {
        Console.WriteLine("Обработка метаданных: валидация и нормализация");
    }
}

class Program
{
    static void Main()
    {
        Data[] dataset = {
            new SignalData(new double[] {1.2, 2.3, 3.4, 4.5}),
            new ProcessedResultData("Пиковое значение: 4.5 В"),
            new AuxiliaryData("Источник: датчик #A42, время: 2023-05-15 14:30")
        };

        foreach (Data data in dataset)
        {
            Console.WriteLine("\n--- Работа с данными ---");
            data.Display();
            data.Process();
            data.Save();
        }
    }
}