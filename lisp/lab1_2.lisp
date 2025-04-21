(setq k 123)
(setq sum (+ (floor k 100) (mod (floor k 10) 10) (mod k 10)))
(format t "Сумма цифр числа ~a: ~a" k sum)