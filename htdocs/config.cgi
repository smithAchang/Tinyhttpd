#!/bin/bash
        #echo "pwd:$(pwd)"
        
        #for debug
        readconfig()
        {
                if [ -r ./config.cfg ];then
                   source  ./config.cfg
                fi

                if [ -r ./htdocs/config.cfg ];then
                    source  ./htdocs/config.cfg
                fi
     
        }
      
       
        echo "Content-Type: text/html;charset=utf-8"
        echo

        #HTTP headers and content must be splitted by two EOLs
        if [ "$REQUEST_METHOD" = "GET" ] ; then
           readconfig
           #echo  "IP:$IP"
       fi

       if [ "$REQUEST_METHOD" = "POST" ] ; then
          #echo "POST"
          #proc the parameters in body
          if [ -r ./htdocs/lib/proccgi.sh ];then
            DEBUG=1
           export DEBUG
           eval `./htdocs/lib/proccgi.sh $* 2> ./htdocs/proccgi.err`
           # eval `./htdocs/lib/proccgi.sh $*`
           # echo "run here!"
          fi

         #fetch the submit data from proccgi.sh
          sed -i 's/^IP=.*$/IP='$FORM_IPClient'/' ./htdocs/config.cfg
          sed -i 's/^PORT=.*$/PORT='$FORM_PORTClient'/' ./htdocs/config.cfg

          #reload to check modified result
          readconfig
        
       fi

       #the same rsp content
       cat  << HTTP_RSP_BODY
                        <!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Welcome to use shell cgi to modify config</title>

                <!-- Bootstrap -->
                <link href="lib/bootstrap-3.3.7-dist/css/bootstrap.min.css" rel="stylesheet">

                </head>
                <body>
                <h1>  Shell CGI demo to modify config file</h1>
                <FORM class="NetWorkConfigDemo" action="config.cgi" method="POST">
                        <div class="form-group">
                                <label for="IP">IP</label>
                                <input type="text" class="form-control " name="IPClient" placeholder="IP" value="$IP">
                        </div>
                        <br>
                        <div class="form-group">
                                <label for="PORT">PORT </label>
                                <input type="text" class="form-control " name="PORTClient" placeholder="port"  value="$PORT">
                        </div>
                        <br>
                        <input type="submit"  class="btn btn-default submit "></input>
                         <input type="reset"  class="btn btn-default reset "></input>
                </FORM>
                </body>
                
                </html>
HTTP_RSP_BODY
        

        
