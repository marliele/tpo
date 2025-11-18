pipeline 
{
    agent any 
    stages {
        stage('Qemu') 
        {
            steps 
            {
                echo 'Stage Qemu: Cleaning and preparing environment'
                sh 'rm -rf romulus romulus.zip'

				echo 'Stage Qemu: Downloading packages'
				sh 'apt update && apt install -y qemu-system wget unzip chromium chromium-driver chromium-l10n python3 python3-selenium python3-locust python3-requests python3-urllib3'

				echo 'Finding browsers'
				echo "Chromium: \$(which chromium 2>/dev/null || which chromium-browser 2>/dev/null || echo 'NOT FOUND')"
				
                echo 'Stage Qemu: Downloading romulus.zip'
                sh 'wget https://jenkins.openbmc.org/job/ci-openbmc/lastSuccessfulBuild/distro=ubuntu,label=docker-builder,target=romulus/artifact/openbmc/build/tmp/deploy/images/romulus/*zip*/romulus.zip'
                sh 'unzip romulus.zip'
                
                echo 'Stage Qemu: Starting QEMU emulator'
                sh ''' 
                    LATEST_MTD=$(ls romulus/obmc-phosphor-image-romulus-*.static.mtd | sort -V | tail -1)
                    echo "Using MTD file: $LATEST_MTD"
                    
                    qemu-system-arm \
                        -m 256 \
                        -M romulus-bmc \
                        -nographic \
                        -drive file=$LATEST_MTD,format=raw,if=mtd \
                        -net nic \
                        -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:623-:623 \
                        > qemu_output.log 2>&1 &
                        
                    QEMU_PID=$!
                    echo "QEMU started with PID: $QEMU_PID"
                    echo $QEMU_PID > qemu.pid
                    
                    echo "Waiting for QEMU to boot..."
                    sleep 60
                    
                    if ps -p $QEMU_PID > /dev/null; then
                        echo "QEMU is running successfully"
                    else
                        echo "ERROR: QEMU process died"
                        echo "QEMU output:"
                        cat qemu_output.log
                        exit 1
                    fi
                '''
            }
        }
        
        stage('Selenium') {
            steps {
                echo 'Stage Selenium: Running Selenium autotests'
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh '''
                        echo "Running Selenium autotests:"
                        cd lab4
                        which chromium-browser || which google-chrome || echo "Chrome not found"
			python3 openbmc_auth_tests.py >> ../selenium_results.txt 2>&1 || echo "Selenium autotests finished with exit code: $?"  
                        echo "Selenium autotests output:"
                        cat ../selenium_results.txt
                    '''
                    archiveArtifacts 'selenium_results.txt'
                }
            }
        }

        stage('Locust') {
            steps {
                echo 'Stage Locust: Running Locust tests'
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh '''
                        echo "Running Locust tests:"
                        cd lab6
                        timeout 60 locust --headless --users 1 --spawn-rate 1 --run-time 30s --host=https://127.0.0.1:2443 > ../locust_results.txt 2>&1 || echo "Locust tests finished with exit code: $?"
                        echo "Locust tests output:"
                        cat ../locust_results.txt
                    '''
                    archiveArtifacts 'locust_results.txt'
                }
            }
        }
        stage('Stop Qemu') 
        {
            steps 
            {
                echo 'Stage Stop Qemu: Stopping QEMU emulation and cleaning up'
                sh '''
                    if [ -f "qemu.pid" ]; then
                        QEMU_PID=$(cat qemu.pid)
                        kill $QEMU_PID 2>/dev/null || true
                        rm -f qemu.pid
                        echo "QEMU stopped"
                    fi
                    rm -rf romulus/ romulus.zip || true
                    rm -f *.log *.pid *.json *.csv || true
                '''
            }
        }
    }
    post 
    {
        always 
        {
            echo 'Archiving all test-related text files...'
            archiveArtifacts artifacts: '**/*.txt', fingerprint: true
            echo 'Pipeline finished.'
        }
    }
}
