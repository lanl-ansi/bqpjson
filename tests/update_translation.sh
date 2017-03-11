rm data/valid/*.qh
rm data/valid/*.qubo
rm data/valid/*.mzn

for file in $(find data/valid -name *.json); do
    cat $file | ../bqpjson/bqp2qh.py > ${file//.json/.qh}
    cat $file | ../bqpjson/spin2bool.py | ../bqpjson/bqp2qubo.py > ${file//.json/.qubo}
    cat $file | ../bqpjson/bqp2mzn.py > ${file//.json/.mzn}
done
