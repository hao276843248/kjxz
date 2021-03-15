server=/root/kjxz
cd $server
echo "git pull ......"
git pull
workon flask # 进入本地环境
verion=$(git rev-parse HEAD)

PID=""
RestartServer=false
status=$(grep $verion ./version.txt)
if [ -z "$status" ]; then
  echo "版本更新,重新部署~"
  echo "记录版本号...."
  echo $verion >./version.txt
  RestartServer=true
else
  echo "版本未更新~"
fi

echo "检测服务是否运行..."
PID=$(ps -ef | grep python | grep app2.py | awk '{ print $2 }')
if [ -z "$PID" ]; then
  echo "服务未运行...."
else
  echo "服务运行中...."
  if [ "$RestartServer"==true ]; then
    echo "删除服务...."
    kill -9 $PID
    echo "killed "+$PID+""
  fi
fi

PID=$(ps -ef | grep python3 | grep app2.py | awk '{ print $2 }')
if [ -z "$PID"]; then
  python app2.py >>log.log 2>&1 &
  echo "启动服务...."
fi
echo "服务正在运行...."
