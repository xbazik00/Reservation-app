#!/usr/bin/bash

# Test cases
# Correct
test_batch=("./book_flight.py --date 2018-04-13 --from BCN --to DUB --one-way")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from LHR --to DXB")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from LHR --to DXB --return 5")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from NRT --to SYD --bags 2")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from CPH --to MIA --fastest --bags 3")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-25 --from CPH --to MIA --cheapest")

CORRECT=${#test_batch[@]}

# False
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from CTT --to MIA")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-33 --from CPH --to MIA")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags -5")
test_batch=("${test_batch[@]}" "./book_flight.py --date 2018-04-13 --from LHR --to DXB --return -1")

number_of_correct=0
for (( i = 0; i < ${#test_batch[@]}; i++ )); do
    printf "**** Running: ${test_batch[$i]} ---- \t"

    RESULT=`${test_batch[$i]}`
    exit_code=$?

    if [ -n "$RESULT" ]; then
        printf "$RESULT ---- \t"
        if (("$i" < "$CORRECT")); then
            if [ ${#RESULT} == 7 ]; then   # Correct result
                number_of_correct=$((number_of_correct + 1))
                echo "OK"
            else                           # Incorrect result
                echo "ERROR"
            fi
        else
            if [ "$RESULT" == "0" ]; then  # Correct result
                number_of_correct=$((number_of_correct + 1))
                echo "OK"
            else                           # Incorrect result
                echo "ERROR"
            fi
        fi
    fi
done

printf "Number of correct evaluations $number_of_correct / ${#test_batch[@]}\n"