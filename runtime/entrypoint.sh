#!/bin/bash

set -euxo pipefail

main () {
    expected_filename=main.sh
    data_directory=/code_execution/data
    cd /code_execution

    submission_files=$(zip -sf ./submission/submission.zip)
    if ! grep -q ${expected_filename}<<<$submission_files; then
        echo "Submission zip archive must include $expected_filename"
    return 1
    fi

    echo Unpacking submission
    unzip ./submission/submission.zip -d ./workdir

    echo Printing submission contents
    find workdir

    pushd workdir

    for (( i=1; i<=30; i++ ))
    do
        # Check if the directory is not empty
        if [ "$(ls -A $data_directory)" ]; then
            echo "Data directory contains files after waiting $i seconds."
            break
        else
            # Sleep for 1 second if the directory is still empty
            sleep 1
        fi
    done
    # if directory is still empty after all attempts, log an error and exit
    if [ ! "$(ls -A $data_directory)" ]; then
        echo "Error: Data directory not properly mounted after waiting 30 seconds."
        exit 1
    fi

    sh main.sh
    popd

    # test the submission
    pytest --no-header -vv tests/test_submission.py
}

main |& tee "/code_execution/submission/log.txt"
exit_code=${PIPESTATUS[0]}

cp /code_execution/submission/log.txt /tmp/log

exit $exit_code