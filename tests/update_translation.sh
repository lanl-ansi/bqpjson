rm data/valid/bool/*.qh
rm data/valid/bool/*.qubo
rm data/valid/bool/*.mzn

rm data/valid/spin/*.qh
rm data/valid/spin/*.qubo
rm data/valid/spin/*.mzn

for file in $(find data/valid/spin -name *.json); do
    cat $file | ../bqpjson/bqp2qh.py > ${file//.json/.qh}
    cat $file | ../bqpjson/spin2bool.py | ../bqpjson/bqp2qubo.py > ${file//.json/.qubo}
    cat $file | ../bqpjson/bqp2mzn.py > ${file//.json/.mzn}
done

for file in $(find data/valid/bool -name *.json); do
    cat $file | ../bqpjson/spin2bool.py | ../bqpjson/bqp2qh.py > ${file//.json/.qh}
    cat $file | ../bqpjson/bqp2qubo.py > ${file//.json/.qubo}
    cat $file | ../bqpjson/bqp2mzn.py > ${file//.json/.mzn}
done