// Chart js | script to populate stacked horizontal bar chart for validation results
document.addEventListener('DOMContentLoaded', function() {
    var labels = [];
    var pct_pattern_mismatch = [];
    var pct_null_values = [];
    var pct_good_data = [];
    var pct_column_notfound = [];
    var pct_dtype_issue = [];
    var pct_neg_values = [];
    var pct_value_notdatetime = [];
    var pct_value_unknown = [];

    // Extract data from JSON
    jsonData.forEach(function(item) {
        labels.push(item.column);
        pct_pattern_mismatch.push(item.pct_pattern_mismatch);
        pct_null_values.push(item.pct_null_values);
        pct_good_data.push(item.pct_good_data);
        pct_column_notfound.push(item.pct_column_notfound);
        pct_dtype_issue.push(item.pct_dtype_issue);
        pct_neg_values.push(item.pct_neg_values);
        pct_value_notdatetime.push(item.pct_value_notdatetime);
        pct_value_unknown.push(item.pct_value_unknown);
    });

    new Chart(
        document.getElementById('validationbar'), {
        type: 'bar',
        data: {
        labels: labels,
        datasets: [{
            label: 'Pattern Issue',
            data: pct_pattern_mismatch,
            backgroundColor: "rgba(152, 134, 123, 0.75)", // Maroon shade
            hoverBackgroundColor: "rgba(152, 134, 123, 1)",
            barPercentage:0.65,
        }, {
            label: 'Null Values',
            data: pct_null_values,
            backgroundColor: "rgba(109, 104, 117, 0.75)", // Gray shade
            hoverBackgroundColor: "rgba(109, 104, 117, 1)",
            barPercentage:0.65,
        }, {
            label: "Good Data",
            data: pct_good_data,
            backgroundColor: "rgba(40, 75, 99, 0.75)", // Blue shade
            hoverBackgroundColor: "rgba(40, 75, 99, 1)",
            barPercentage:0.65,
        }, {
            label: "Column_unavailable",
            data: pct_column_notfound,
            backgroundColor: "rgba(255, 205, 178, 0.75)", // Light Maroon shade
            hoverBackgroundColor: "rgba(255, 205, 178, 1)",
            barPercentage:0.65,
        }, {
            label: "DataType Issue",
            data: pct_dtype_issue,
            backgroundColor: "rgba(111, 67, 76,0.75)", // The original color
            hoverBackgroundColor: "rgba(111, 67, 76,1)",
            barPercentage:0.65,
        }, {
            label: "Found Negative Values",
            data: pct_neg_values,
            backgroundColor: "rgba(255, 180, 162, 0.75)", // Reddish shade
            hoverBackgroundColor: "rgba(255, 180, 162, 1)",
            barPercentage:0.65,
        }, {
            label: "Not Datetime",
            data: pct_value_notdatetime,
            backgroundColor: "rgba(229, 152, 155, 0.75)", // Reddish shade
            hoverBackgroundColor: "rgba(229, 152, 155, 1)",
            barPercentage:0.65,
        }, {
            label: "Unknown value",
            data: pct_value_unknown,
            backgroundColor: "rgba(235, 152, 155, 0.75)", // Reddish shade
            hoverBackgroundColor: "rgba(235, 152, 155, 1)",
            barPercentage:0.65,
        }]
        
        },
        options: {
        indexAxis: 'y',
        scales: {
            x: {
            stacked: true
            },
            y: {
            stacked: true
            }
        },
        plugins: {
            legend: {
            display: true,
            position: 'top', // Place the legend to the top
            align: 'end', // Place the legend to the right end 
            labels: {
                // Use 'dataset' to display dataset labels instead of 'undefined'
                generateLabels: function (chart) {
                var datasets = chart.data.datasets;
                var labels = chart.data.labels;
                var legends = [];

                datasets.forEach(function (dataset, datasetIndex) {
                    // Check if any non-zero value is present in the dataset
                    var hasNonZeroValue = dataset.data.some(function(value) {
                        return value !== 0;
                    });
    
                    if (hasNonZeroValue) {
                        legends.push({
                            text: dataset.label,
                            fillStyle: dataset.backgroundColor,
                            hidden: !chart.isDatasetVisible(datasetIndex),
                            lineCap: dataset.borderCapStyle,
                            lineDash: dataset.borderDash,
                            lineDashOffset: dataset.borderDashOffset,
                            lineJoin: dataset.borderJoinStyle,
                            lineWidth: dataset.borderWidth,
                            strokeStyle: dataset.borderColor,
                            pointStyle: dataset.pointStyle,
                            rotation: dataset.rotation,
                            datasetIndex: datasetIndex
                        });
                    }
                });
                return legends;
                }
            },
            }
        },
        },
    })
});

// Chart js | script to populate doughnut chart 
document.addEventListener('DOMContentLoaded', function() {
    
    var data = {
        labels: ['Structured', 'Unstructured'],
        datasets: [{
            data: [58, 42],
            backgroundColor: ['rgba(63,103,126,1)', 'rgba(163,103,126,1)', 'rgba(63,203,226,1)', 'rgba(90,34,21,1)', 'rgba(200,150,50,1)', 'rgba(235,91,56,1)', 'rgba(137,196,244,1)', 'rgba(245,203,83,1)', 'rgba(142,69,173,1)', 'rgba(76,175,80,1)'],
            hoverBackgroundColor: ['rgba(50,90,100,1)', 'rgba(140,85,100,1)', 'rgba(46,185,235,1)', 'rgba(45,21,231,1)', 'rgba(190,120,40,1)', 'rgba(205,80,47,1)', 'rgba(101,154,204,1)', 'rgba(221,183,60,1)', 'rgba(110,49,147,1)', 'rgba(60,136,63,1)']
        }]
    };

    new Chart(document.getElementById('doughnutchart_strvsunstr'), {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    align: 'center',
                }
            },
            tooltips: {
                callbacks: {
                    label: function (context) {
                        var label = context.label || '';
                        var value = context.formattedValue;
                        return label + ': ' + value;
                    }
                }
            }
        }
    });
});

// Chart js | script to populate doughnut chart 
document.addEventListener('DOMContentLoaded', function() {
    var ranks = [];
    var cnt_rank_employee = [];

    // Extract data from JSON
    json_rankwise_empdist.forEach(function(item) {
        ranks.push(item.Rank);
        cnt_rank_employee.push(item.count_rank);
    });


    var data = {
        labels: ranks,
        datasets: [{
            data: cnt_rank_employee,
            backgroundColor: ['rgba(63,103,126,1)', 'rgba(163,103,126,1)', 'rgba(63,203,226,1)', 'rgba(90,34,21,1)', 'rgba(200,150,50,1)', 'rgba(235,91,56,1)', 'rgba(137,196,244,1)', 'rgba(245,203,83,1)', 'rgba(142,69,173,1)', 'rgba(76,175,80,1)'],
            hoverBackgroundColor: ['rgba(50,90,100,1)', 'rgba(140,85,100,1)', 'rgba(46,185,235,1)', 'rgba(45,21,231,1)', 'rgba(190,120,40,1)', 'rgba(205,80,47,1)', 'rgba(101,154,204,1)', 'rgba(221,183,60,1)', 'rgba(110,49,147,1)', 'rgba(60,136,63,1)']
        }]
    };

    new Chart(document.getElementById('doughnutChart'), {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    align: 'center',
                }
            },
            tooltips: {
                callbacks: {
                    label: function (context) {
                        var label = context.label || '';
                        var value = context.formattedValue;
                        return label + ': ' + value;
                    }
                }
            }
        }
    });
});

// Badges | Doughnut chart script for pillar distribution 
document.addEventListener('DOMContentLoaded', function() {
    var pillar = [];
    var pct_gui = [];
    json_pillar_data.forEach(function(item) {
        pillar.push(item.Pillar);
        pct_gui.push(item.pct_gui);
    });

    var data = {
        labels: pillar,
        datasets: [{
            data: pct_gui,
            backgroundColor: ['rgba(63,103,126,1)', 'rgba(163,103,126,1)', 'rgba(63,203,226,1)', 'rgba(90,34,21,1)', 'rgba(200,150,50,1)'],
            hoverBackgroundColor: ['rgba(50,90,100,1)', 'rgba(140,85,100,1)', 'rgba(46,185,235,1)', 'rgba(45,21,231,1)', 'rgba(190,120,40,1)']
        }]
    };

    new Chart(document.getElementById('doughnutChart2'), {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    align: 'center',
                }
            },
            tooltips: {
                callbacks: {
                    label: function (context) {
                        var label = context.label || '';
                        var value = context.formattedValue;
                        return label + ': ' + value;
                    }
                }
            }
        }
    });
});

// Badges | Bar chart for badge earned per month
document.addEventListener('DOMContentLoaded', function() {
    var month = [];
    var cnt_gui_badgeinitiated = [];
    var cnt_gui_badgeawarded = [];

    json_badgecompletion_data.forEach(function(item) {
        month.push(item.Month);
        cnt_gui_badgeinitiated.push(item.cnt_gui_badgeinitiated);
        cnt_gui_badgeawarded.push(item.cnt_gui_badgeawarded);
    }); 

    new Chart(document.getElementById('barchart_badgecompletionpermonth'), {
        type: 'line',
        data: {
            labels: month,
            datasets: [{
                label: 'BadgeInitiated',
                data: cnt_gui_badgeinitiated,
                borderColor: 'rgba(154, 59, 59, 0.55)',
                backgroundColor: 'rgba(154, 59, 59, 0.2)',
                borderWidth: 7,
                pointRadius: 4,
                pointHoverRadius: 7,
                fill:true,
                
            },{
                label: 'BadgeAwarded',
                data: cnt_gui_badgeawarded,
                borderColor: 'rgba(38,87,124, 0.55)',
                backgroundColor: 'rgba(38,87,124,0.2)',
                borderWidth: 7,
                pointRadius: 4,
                pointHoverRadius: 7,
                fill:true,
            },
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
        },
        
    });
});

document.addEventListener('DOMContentLoaded', function() {
    new Chart(document.getElementById('doughnutChart4'), {
        type: 'doughnut',
        data: data,
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'right',
                }
            },
            tooltips: {
                callbacks: {
                    label: function (context) {
                        var label = context.label || '';
                        var value = context.formattedValue;
                        return label + ': ' + value;
                    }
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Chart js | populating the line chart across each month with their rank
    // Get the canvas element and context for the line chart
    var labels = [];
    var dist_staff = [];
    var dist_senior = [];
    var dist_manager = [];
    var dist_seniormanager = [];
    var dist_director = [];
    var dist_partner = [];

    // Extract data from JSON
    jsonEmpDist.forEach(function(item) {
        labels.push(item.Month);
        dist_staff.push(item.Staff);
        dist_senior.push(item.Senior);
        dist_manager.push(item.Manager);
        dist_seniormanager.push(item.SeniorManager);
        dist_director.push(item.Director);
        dist_partner.push(item.Partner);
    });

    var canvas = document.getElementById('line_rankdistribution');
    var ctx = canvas.getContext('2d');
    // Data for the multiple line charts                  
    var data = {
        labels: labels,
        datasets: [
            {
                label: 'Staff',
                data: dist_staff,
                borderColor: 'rgba(0, 102, 153, 0.5)',
                backgroundColor: 'rgba(0, 102, 153, 0.2)',
                borderWidth: 7,
                pointRadius: 7,
                pointHoverRadius: 8,
                // fill:true,
            },
            {
                label: 'Senior',
                data: dist_senior,
                borderColor: 'rgba(0, 204, 204, 0.5)',
                backgroundColor: 'rgba(0, 204, 204,0.2)',
                borderWidth: 7,
                pointRadius: 7,
                pointHoverRadius: 8,
                // fill: true,
            },
            // {
            //     label: 'Manager',
            //     data: dist_manager,
            //     borderColor: 'rgba(204, 102, 0, 0.5)',
            //     // backgroundColor: 'rgba(77, 255, 255,0.2)',
            //     borderWidth: 5,
            //     pointRadius: 5,
            //     // pointHoverRadius: 6,
            // },
            {
                label: 'Senior Manager',
                data: dist_seniormanager,
                borderColor: 'rgba(255, 204, 102, 0.5)',
                backgroundColor: 'rgba(255, 204, 102,0.2)',
                borderWidth: 7,
                pointRadius: 7,
                pointHoverRadius: 8,
                // fill:true,
            },
            // {
            //     label: 'Director',
            //     data: dist_director,
            //     borderColor: 'rgba(34, 62, 119,0.5)',
            //     // backgroundColor: 'rgba(193, 240, 240,0.2)',
            //     borderWidth: 5,
            //     pointRadius: 6,
            //     // pointHoverRadius: 6,
            // },
            // {
            //     label: 'Partner/Principal',
            //     data: dist_partner,
            //     borderColor: 'rgba(34, 62, 119,0.7)',
            //     // backgroundColor: 'rgba(255, 245, 204,0.2)',
            //     borderWidth: 5,
            //     pointRadius: 5,
            //     // pointHoverRadius: 6,
            // },
            // Add more datasets for additional line charts if needed
            {
                label: 'Total Count',
                data: [55, 60, 65, 50, 60, 61, 50],
                backgroundColor: 'rgba(63,103,126,0.8)',
                borderWidth: 1,
                barPercentage: 0.6,
                categoryPercentage: 0.8,
                type: 'bar'
            },
        ]
    };

    // Create the line chart
    var lineChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            elements: {
                line: {
                    tension: 0.4, // Adjust the tension for smooth curves
                },
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                    },
                },
                y: {
                    beginAtZero: true, // Begin y-axis at zero
                    display: true,
                    title: {
                        display: true,
                        text: 'Employee Count',
                    },
                },
            },
        }
    });
});

// Calculate cumulative percentage
document.addEventListener('DOMContentLoaded', function() {
    var data = {
        labels: ['Bengaluru', 'Mumbai', 'Kolkata', 'Hyderabad', 'Gurgaon', 'Noida', 'Pune'],
        datasets: [
            {
                label: 'Employee Count',
                data: [2541, 1965, 1809, 1592, 1294, 762, 147],
                backgroundColor: 'rgba(0, 68, 102, 0.7)',
                yAxisID: 'primary',
                barPercentage: 0.6,
            },
            {
                label: 'Cumulative Percentage',
                data: [25,44,62, 78, 91, 99, 100],
                borderColor: 'rgba(163,103,126,0.7)',
                backgroundColor: 'transparent',
                borderWidth: 4,
                pointRadius: 5,
                yAxisID: 'secondary',
                type: 'line',
            },
        ],
    };

    // Get the canvas context
    var ctx = document.getElementById('pareto_citydistribution').getContext('2d');

    // Create the multi-axis Pareto diagram with options
    var pareto_citydistribution = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'City',
                    },
                },
                primary: {
                    type: 'linear',
                    position: 'left',
                    beginAtZero: true,
                    display: true,
                    title: {
                        display: true,
                        text: 'Employee Count',
                    },
                },
                secondary: {
                    type: 'linear',
                    position: 'right',
                    beginAtZero: true,
                    display: true,
                    title: {
                        display: true,
                        text: 'Cumulative Percentage',
                    },
                },
            },
            plugins: {
                legend: {
                    display: true,
                },
            },
        },
    });
});

// chat function which loads user message and gets bot response by invoking the URI
document.addEventListener("DOMContentLoaded", function () {
    const msgerForm = document.querySelector(".msger-inputarea");
    const msgerInput = document.querySelector("#textInput");
    const msgerChat = document.querySelector(".chat-container");
  
    msgerForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const msgText = msgerInput.value;
      if (!msgText) return;
  
      appendMessage(msgText);
      msgerInput.value = "";
      botResponse(msgText);
    });
  
    function appendMessage(text) {
      const msgHTML = `
        <div class="user-message">
          <div class="user-icon"></div>
          <div class="user-message-bubble">
            ${text}
          </div>
        </div>
      `;
      
      msgerChat.insertAdjacentHTML("beforeend", msgHTML);
      msgerChat.scrollTop += 500;
    }
  
    function botResponse(rawText) {

        // const table_selected = document.getElementById("table-dropdown").value;
        const url = window.location.href;
        const parts = url.split('/');
        const lastPart = parts[parts.length - 1];
        // Remove any query parameters (e.g., '?foo=bar') by splitting at '?'
        const withoutQuery = lastPart.split('?')[0];
        // Assign the substring to table_selected
        table_selected = withoutQuery.replace('validate_', '');;
  
      $.get("/get_val_llmresponse", { msg: rawText, table_selected: table_selected }).done(function (data) {
        // Create a new Date object to represent the current date and time
        const currentDate = new Date();
        // Get various components of the current date and time
        const year = currentDate.getFullYear();        // Get the current year (e.g., 2023)
        const month = currentDate.getMonth() + 1;      // Get the current month (0-11, add 1 for January to December)
        const day = currentDate.getDate();             // Get the current day of the month (1-31)
        const hours = currentDate.getHours();           // Get the current hour (0-23)
        const minutes = currentDate.getMinutes();       // Get the current minute (0-59)
        const seconds = currentDate.getSeconds();       // Get the current second (0-59)
        const milliseconds = currentDate.getMilliseconds(); // Get the current millisecond (0-999)
        const timestamp_now = `${year}${month}${day}-${hours}${minutes}${seconds}${milliseconds}`
        const canvasid = "canvasid_" + timestamp_now
        
        var responseData = JSON.parse(data);

        var issuccess = responseData.success;
        var chart_type = responseData.chart_type;
        var chart_label = responseData.chart_label;
        var text_to_display = responseData.text_to_display;

        if (chart_type === 'text') {
            if (text_to_display === null || text_to_display === '') {
                text_to_display = '<span class="badge badge-danger">Error</span> Please try modifying the prompt with more details.';
            }
          }
        
        var chart_data = JSON.parse(responseData.chart_json_data);

        const msgHTML = `
          <div class="bot-message">
            <div class="bot-icon"></div>
            <div class="bot-message-bubble">
            ${chart_type !=='text' ? `<canvas id="${canvasid}" height="235"></canvas>` : text_to_display}
            </div>
          </div>
        `;
        msgerChat.insertAdjacentHTML("beforeend", msgHTML);
        msgerChat.scrollTop += 500;

        // Create the chart for this message
        new Chart(document.getElementById(canvasid), {
            // type: 'line',
            data: chart_data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        align: 'center',
                    },
                },
            }
        });
      });
    }
  });
  

// Miscellanous | Bar chart count of GUI matching with 
document.addEventListener('DOMContentLoaded', function() {
    var tableinconsideration = ['Workforce', 'GTE', 'TR', 'Badges', 'Learning', 'LAT', 'WorkExperience'];
    var pct_commongui = [100, 98, 73, 89, 75, 70, 78];

    // json_badgecompletion_data.forEach(function(item) {
    //     month.push(item.Month);
    //     cnt_gui_badgeinitiated.push(item.cnt_gui_badgeinitiated);
    //     cnt_gui_badgeawarded.push(item.cnt_gui_badgeawarded);
    // }); 

    new Chart(document.getElementById('alltable_matchbar'), {
        type: 'bar',
        data: {
            labels: tableinconsideration,
            datasets: [{
                label: 'Percentage of GUIs matching with other tables',
                data: pct_commongui,
                borderColor: 'rgba(0, 68, 102, 0.8)',
                backgroundColor: pct_commongui.map(value => value < 75 ? '#EE9322' : 'rgba(0, 68, 102, 0.6)'),
                barPercentage: 0.65
            }]
        },
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true
                }
            },
            plugins: {
                verticalLine: {
                    x: 75, // The x-coordinate where you want to draw the line
                    borderColor: '#FF9B50', // Line color
                    borderWidth: 4, // Line width
                    label: {
                        text: '75%', // Label text
                        position: 'top', // Label position
                        backgroundColor: 'white', // Label background color
                    },
                }
            },
        },
        
    plugins: [{
        beforeDraw: (chart) => {
            const line = chart.options.plugins.verticalLine;
            if (line) {
                const ctx = chart.ctx;
                const x = chart.scales.x.getPixelForValue(line.x);
                // Set the line to be dotted
                ctx.setLineDash([10, 5]); // Adjust the numbers to change the dash pattern

                // Draw the vertical line
                ctx.save();
                ctx.beginPath();
                ctx.strokeStyle = line.borderColor;
                ctx.lineWidth = line.borderWidth;
                ctx.moveTo(x, chart.chartArea.top);
                ctx.lineTo(x, chart.chartArea.bottom);
                ctx.stroke();
                ctx.restore();

                // Draw the label
                if (line.label) {
                    const labelX = x + 5; // Adjust the label's x-coordinate for proper positioning
                    const labelY = chart.chartArea.top + 145; // Adjust the label's y-coordinate for proper positioning

                    ctx.fillStyle = line.label.backgroundColor;
                    ctx.fillRect(labelX, labelY, 25, 15);

                    ctx.textAlign = 'left';
                    ctx.font = '12px Arial';
                    ctx.fillStyle = 'black';
                    ctx.fillText(line.label.text, labelX + 5, labelY + 12);
                }
            }
        }
    }],
});
})