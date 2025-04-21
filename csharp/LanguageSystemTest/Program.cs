using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

public class LanguageData
{
    private List<string> _syllables = new List<string>();

    public int LanguageId { get; }
    public int MinSyllables { get; } = 2;
    public int MaxSyllables { get; } = 5;

    public List<string> Syllables
    {
        get => _syllables;
        set => _syllables = value?.Count > 0 ? value : throw new ArgumentException("Language must have syllables");
    }


    public LanguageData(int id, List<string> syllables,
                       int minSyllables = 2, int maxSyllables = 5)
    {
        if (minSyllables > maxSyllables)
            throw new ArgumentException("Min syllables cannot exceed max");

        LanguageId = id;
        Syllables = syllables;
        MinSyllables = minSyllables;
        MaxSyllables = maxSyllables;
    }
}

public static class LanguageStorage
{
    public static Dictionary<int, LanguageData> Languages = new Dictionary<int, LanguageData>();
}

public class SpeechMessage
{
    public required string OriginalText;
    public int LanguageId;
    public required Player Sender;
}

public static class TextTokenizer
{
    private static readonly Regex TokenRegex = new Regex(
        @"(\s+)|(\w+[\-']*\w+)|(\p{L}+)|([^\s\p{L}]+)",
        RegexOptions.Compiled | RegexOptions.IgnoreCase
    );

    public static List<Token> Tokenize(string text)
    {
        var tokens = new List<Token>();
        foreach (Match match in TokenRegex.Matches(text))
        {
            string value = match.Value;

            // Определяем тип токена
            bool isSpace = match.Groups[1].Success;
            bool isWord = !isSpace && (match.Groups[2].Success || match.Groups[3].Success);

            tokens.Add(new Token(
                Value: value,
                IsWord: isWord,
                IsWhitespace: isSpace
            ));
        }
        return tokens;
    }
}

public record Token(string Value, bool IsWord, bool IsWhitespace = false);

public class Player
{
    public required string Name;
    public List<int> KnownLanguages = new List<int>();

    public bool KnowsLanguage(int languageId) => KnownLanguages.Contains(languageId);

    public void SendMessage(string text, int languageId, Player receiver)
    {
        var message = new SpeechMessage
        {
            OriginalText = text,
            LanguageId = languageId,
            Sender = this
        };

        ProcessMessage(message, receiver);
    }

    private void ProcessMessage(SpeechMessage message, Player receiver)
    {
        if (receiver.KnowsLanguage(message.LanguageId))
        {
            DisplayMessage(message.OriginalText, receiver);
            return;
        }

        string translated = LanguageTranslator.Translate(message);
        DisplayMessage(translated, receiver);
    }

    private void DisplayMessage(string text, Player receiver)
    {
        Console.WriteLine($"[{receiver.Name}] Received: {text}");
    }
}

public static class LanguageTranslator
{
    public static string Translate(SpeechMessage message)
    {
        if (!LanguageStorage.Languages.TryGetValue(message.LanguageId, out var langData))
            return message.OriginalText;

        var tokens = TextTokenizer.Tokenize(message.OriginalText);
        var result = new StringBuilder();

        foreach (var token in tokens)
        {
            if (token.IsWhitespace)
            {
                result.Append(token.Value); // Сохраняем пробелы как есть
            }
            else if (token.IsWord)
            {
                string translatedWord = TranslateWord(token.Value, langData);
                result.Append(translatedWord);
            }
            else
            {
                result.Append(token.Value);
            }
        }

        return result.ToString();
    }

    private static string TranslateWord(string originalWord, LanguageData langData)
    {
        // Сохраняем оригинальный регистр до нормализации
        bool isAllUpper = originalWord.All(c => !char.IsLetter(c) || char.IsUpper(c));
        bool isFirstUpper = char.IsUpper(originalWord[0]);

        string cleanWord = originalWord.ToLowerInvariant().Trim();
        if (string.IsNullOrEmpty(cleanWord)) return originalWord;

        int hash = GetStableHash(cleanWord);
        var sb = new StringBuilder();

        // Генерация слогов (существующая логика)
        for (int i = 0; i < 4; i++)
        {
            int syllableIndex = Math.Abs(
                (hash >> (i * 8)) % langData.Syllables.Count
            );
            sb.Append(langData.Syllables[syllableIndex]);
        }

        // Применяем регистр
        string result = sb.ToString();
        
        if (isAllUpper)
        {
            result = result.ToUpperInvariant();
        }
        else if (isFirstUpper)
        {
            result = char.ToUpper(result[0]) + result.Substring(1).ToLower();
        }
        else
        {
            result = result.ToLower();
        }

        return result;
    }

    private static int GetStableHash(string text)
    {
        string normalizedText = text.ToLowerInvariant();

        unchecked
        {
            int hash = 5381;
            foreach (char c in normalizedText)
            {
                hash = (hash << 5) + hash + c;
            }
            return hash;
        }
    }
}

// Пример использования
class Program
{
    static void Main()
    {
        // Создаем язык
        var elvish = new LanguageData(
            id: 1,
            syllables: new List<string> { "mel", "lor", "nin", "dor", "tho", "las" }
        );
        var dragonish = new LanguageData(
            id: 2,
            syllables: new List<string> { "vok", "drak", "zul", "mahr", "thu" },
            minSyllables: 2,
            maxSyllables: 4
        );
        var rude = new LanguageData(
            id: 3,
            syllables: new List<string> { "ug", "ba", "gro", "thu", "nak", "zug", "bru" },
            minSyllables: 2,
            maxSyllables: 3
        );
        var egiptian = new LanguageData(
            id: 4,
            syllables: new List<string> { "ra", "anub", "sekh", "phara", "nile", "seth", "isis" },
            minSyllables: 3,
            maxSyllables: 3
        );
        LanguageStorage.Languages.Add(elvish.LanguageId, elvish);
        LanguageStorage.Languages.Add(dragonish.LanguageId, dragonish);
        LanguageStorage.Languages.Add(rude.LanguageId, rude);
        LanguageStorage.Languages.Add(egiptian.LanguageId, egiptian);

        // Создаем игроков
        var player1 = new Player { Name = "Player1", KnownLanguages = { 3 } };
        var player2 = new Player { Name = "Player2", KnownLanguages = { } };

        // Отправляем сообщение
        string word = "Добрый день, как поживаете?";
        player1.SendMessage(word, 2, player2); // Gimli увидит "lorlasninmel"
        player1.SendMessage(word, 2, player1); // Legolas увидит "Привет"
    }
}