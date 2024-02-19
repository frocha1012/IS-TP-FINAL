package main

import (
    "database/sql"
    "fmt"
    "log"
    "time"

    _ "github.com/lib/pq"
    "github.com/streadway/amqp"
)

func failOnError(err error, msg string) {
    if err != nil {
        log.Fatalf("%s: %s", msg, err)
    }
}

const (
    DBHost        = "db-xml"
    DBName        = "is"
    DBUser        = "is"
    DBPassword    = "is"
    RabbitMQHost  = "broker"
    RabbitMQUser  = "is"
    RabbitMQPass  = "is"
    RabbitMQVHost = "is"
    PollingFreq   = 5 // Polling seconds
)

func main() {
    // Database connection
    connStr := fmt.Sprintf("host=%s dbname=%s user=%s password=%s sslmode=disable", DBHost, DBName, DBUser, DBPassword)
    db, err := sql.Open("postgres", connStr)
    failOnError(err, "Failed to connect to PostgreSQL")
    defer db.Close()

    // RabbitMQ connection
    amqpURI := fmt.Sprintf("amqp://%s:%s@%s/%s", RabbitMQUser, RabbitMQPass, RabbitMQHost, RabbitMQVHost)
    conn, err := amqp.Dial(amqpURI)
    failOnError(err, "Failed to connect to RabbitMQ")
    defer conn.Close()

    ch, err := conn.Channel()
    failOnError(err, "Failed to open a channel")
    defer ch.Close()

    q, err := ch.QueueDeclare(
        "xml_import_tasks", // queue name
        false,              // durable
        false,              // delete when unused
        false,              // exclusive
        false,              // no-wait
        nil,                // arguments
    )
    failOnError(err, "Failed to declare a queue")

    for {
        rows, err := db.Query("SELECT id, src FROM converted_documents WHERE is_processed = FALSE;")
        failOnError(err, "Failed to execute query")

        var fileID, fileName string
        for rows.Next() {
            err = rows.Scan(&fileID, &fileName)
            failOnError(err, "Failed to read row")

            message := fmt.Sprintf("Process file: %s with id: %s", fileName, fileID)
            err = ch.Publish(
                "", // exchange
                q.Name, // routing key
                false,  // mandatory
                false,  // immediate
                amqp.Publishing{
                    ContentType: "text/plain",
                    Body:        []byte(message),
                },
            )
            failOnError(err, "Failed to publish a message")

            
            log.Printf("Successfully published message for file: %s with id: %s", fileName, fileID)
        }

        // Check if there were any files to process, and log accordingly
        if rows.NextResultSet() {
            log.Printf("No new files found. Waiting for %d seconds before polling again.", PollingFreq)
        }

        rows.Close() // memory leak prevention

        time.Sleep(time.Duration(PollingFreq) * time.Second)
    }
}
