(let* ((n 1991)
       (d1 (floor n 1000))
       (d2 (mod (floor n 100) 10))
       (d3 (mod (floor n 10) 10))
       (d4 (mod n 10)))
  (format t "~:[false~;true~]" (= (+ d1 d2) (+ d3 d4))))