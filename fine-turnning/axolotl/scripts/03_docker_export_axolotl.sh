BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

docker save -o axolotl.tar axolotlai/axolotl
