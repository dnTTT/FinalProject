import subprocess


def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


if __name__ == '__main__':
    hello_command = "ipconfig"
    hello_info = run(hello_command)
    if hello_info.returncode != 0:
        print("An error occured: %s", hello_info.stderr)
    else:
        print("Hello command executed successfully!")
        text = hello_info.stdout
        for line in text.splitlines():
            print(line)

        #print(hello_info.stdout)

    print("-------------------------")

    bad_syntax_command = "Write-Hst 'Incorrect syntax command!'"
    bad_syntax_info = run(bad_syntax_command)
    if bad_syntax_info.returncode != 0:
        print("An error occured: %s", bad_syntax_info.stderr)
    else:
        print("Bad syntax command executed successfully!")