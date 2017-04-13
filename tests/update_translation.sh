# Note that venv should be enabled when running this

rm data/valid/bool/*.qh
rm data/valid/bool/*.qubo
rm data/valid/bool/*.mzn
rm data/valid/bool/*.hfs

rm data/valid/spin/*.qh
rm data/valid/spin/*.qubo
rm data/valid/spin/*.mzn
rm data/valid/spin/*.hfs

for file in $(find data/valid/spin -name *.json); do
    cat $file | bqp2qh > ${file//.json/.qh}
    cat $file | spin2bool | bqp2qubo > ${file//.json/.qubo}
    cat $file | bqp2mzn > ${file//.json/.mzn}
    cat $file | spin2bool | bqp2hfs > ${file//.json/.hfs}
done

for file in $(find data/valid/bool -name *.json); do
    cat $file | spin2bool | bqp2qh > ${file//.json/.qh}
    cat $file | bqp2qubo > ${file//.json/.qubo}
    cat $file | bqp2mzn > ${file//.json/.mzn}
    cat $file | bqp2hfs > ${file//.json/.hfs}
done