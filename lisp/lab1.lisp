(defun ln (x)
  (log x))

(defun sin-power (x power)
  (expt (sin x) power))

(defun function1 (x)
  (+ (* 3 (ln (expt x 2)))
     (* 6 (ln (abs x)))
     -6))

(defun function2 (x)
  (- (+ x (* 3.6 x))
     (sin-power x 7)))

(defun display-functions (x)
  (format t "Для x = ~a:~%" x)
  (format t "  Функция F: ~a~%" (function1 x))
  (format t "  Функция G: ~a~%" (function2 x)))

(display-functions 2)