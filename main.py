import uvicorn


def main() -> None:
    uvicorn.run(
        app="web_server:app",
        reload=True,
        port=8080
    )


if __name__ == '__main__':
    main()
