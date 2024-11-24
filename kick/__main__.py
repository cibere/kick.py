import subprocess

import click


@click.group
def cli(): ...


@cli.group(name="bypass", help="Stuff regarding the cloudflare bypass script")
def bypass(): ...


BYPASS_CODE = """

package main

import (
    "log"
    "strings"
	"bytes"

    "github.com/Danny-Dasilva/CycleTLS/cycletls"
    "github.com/gin-gonic/gin"
)

func sendKickMessage(context *gin.Context) cycletls.Response {
    client := cycletls.Init()
	headers := make(map[string]string)
	for key, values := range context.Request.Header {
	headers[key] = strings.Join(values, ",")
	}

	buf := new(bytes.Buffer)
	buf.ReadFrom(context.Request.Body)
	bodyStr := buf.String()


	url := context.Query("url")
    response, err := client.Do(url, cycletls.Options{
        Body:      bodyStr,
		Headers:   headers,
        Ja3:       "771,4865-4867-4866-49195-49199-52393-52392-49196-49200-49162-49161-49171-49172-51-57-47-53-10,0-23-65281-10-11-35-16-5-51-43-13-45-28-21,29-23-24-25-256-257,0",
        UserAgent: "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
        // PROXY_HERE
    }, context.Request.Method)
    if err != nil {
        log.Print("Request Failed: " + err.Error())
    }
    return response
}

func queryRespone(context *gin.Context) {
    response := sendKickMessage(context)
    context.String(response.Status, response.Body)
}


func main() {
	log.Print("starting")
 	gin.SetMode(gin.ReleaseMode)
    router := gin.Default()

    router.Any("/request", queryRespone)

    router.Run("localhost:9090")
}

"""


@bypass.command(help="Creates the bypass file", name="create")
@click.option(
    "--port",
    default=9090,
    help="The port for the bypass script to run the webserver on",
)
@click.option("--fp", default="bypass.go", help="The filepath for the file to go to")
@click.option(
    "--proxy",
    help="A proxy url in the format of: http://username:password@hostname.tld:port. Rotating proxy not supported",
    default=None,
)
def create_file(port: int, fp: str, proxy: str | None) -> None:
    code = BYPASS_CODE.replace("{port}", f"{port}")
    if proxy:
        code = code.replace(f"// PROXY_HERE", f'Proxy: "{proxy}",')
    with open(fp, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Done writing to {fp}.\nMake sure to install the dependencys.")


@bypass.command(help="installs the script's dependencys", name="install")
def install_dependencys() -> None:
    print("Running go init...")
    subprocess.run(["/usr/bin/go", "mod", "init", "example/project-name"])
    print("Installing CycleTLS...")
    subprocess.run(["go", "get", "github.com/Danny-Dasilva/CycleTLS/cycletls"])
    print("Installing gin...")
    subprocess.run(["go", "get", "github.com/gin-gonic/gin"])
    print("\n\nAll done. Run `go run filepath` to run the file.")


if __name__ == "__main__":
    cli()
