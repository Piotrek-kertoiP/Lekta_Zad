echo "Request data = \"expression\":\" (1+  (-2))*2+3*(1-3+4)+10/2\""
echo "Expected result = 9.0"
curl -H "Content-Type: application/json" -X POST -d '{"expression":" (1+  (-2))*2+3*(1-3+4)+10/2"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"expression\":\"3+4*2/(1-5)\""
echo "Expected result = 1.0"
curl -H "Content-Type: application/json" -X POST -d '{"expression":"3+4*2/(1-5)"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"expression\":\"*(1-1)*2+3*(1-3+4)+10/2\""
echo "Expected result = missing_argument_for_operator"
curl -H "Content-Type: application/json" -X POST -d '{"expression":"*(1-1)*2+3*(1-3+4)+10/2"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = definitely not json data"
echo "Expected result = not json data"
curl -H "Content-Type: application/json" -X POST -d 'definitely not json data' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"expression\":\"(1-d)*2+3*(1-3+4)+10/2\""
echo "Expected result = unallowed characters"
curl -H "Content-Type: application/json" -X POST -d '{"expression":"(1-d)*2+3*(1-3+4)+10/2"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"something_else\":\"(1-1)*2+3*(1-3+4)+10/2\""
echo "Expected result = wrong json data"
curl -H "Content-Type: application/json" -X POST -d '{"something_else":"(1-1)*2+3*(1-3+4)+10/2"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"expression\":\"((1-1)*2+3*(1-3+4)+10/2\""
echo "Expected result = wrong parentheses"
curl -H "Content-Type: application/json" -X POST -d '{"expression":"((1-1)*2+3*(1-3+4)+10/2"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"expression\":\"(1-1)*2+3*(1-3+4)+10/2\""
echo "Expected result = 11"
curl -H "Content-Type: application/json" -X POST -d '{"expression":"(1-1)*2+3*(1-3+4)+10/2"}' http://localhost:5000/evaluate
printf "\n\n"

echo "Request data = \"expression\":\"( 32 - 42 / 95 + 24 ( ) ( 53 ) + ) 21\""
curl -H "Content-Type: application/json" -X POST -d '{"expression":"( 32 - 42 / 95 + 24 ( ) ( 53 ) + ) 21"}' http://localhost:5000/evaluate

echo "Request data = \"expression\":\"2/0\""
curl -H "Content-Type: application/json" -X POST -d '{"expression":"2/0"}' http://localhost:5000/evaluate
