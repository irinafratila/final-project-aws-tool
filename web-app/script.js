function isOlderThanXDays(ageLimit, date) {
    date = date.split(',')[0]
    var dateOfInstance = moment(date, "DD/MM/YYYY")
    var dateXDaysAgo = moment().subtract(ageLimit, 'days')

    return dateOfInstance.isBefore(dateXDaysAgo)
}
function sortByDate(a,b, descOrAsc) {
    if (descOrAsc == 'desc') {
        if (a > b) {
            return 1
        } else {
            return -1
        }
    } else if (descOrAsc == 'asc') {
        if (a < b) {
            return 1
        } else {
            return -1
        }
    } else {
        throw "Invalid option for descending or ascending"
    }
}

function buildInstancesTable(instanceData) {
    var table = document.getElementById('instanceTable');
    table.innerHTML = '';

    /**
     * "for" loop adapted from Dennis Ivy (2019) JSON Array to HTML Table with Javascript
     * Available at https://www.youtube.com/watch?v=XmdOZ5NSqb8&list=PL-51WBLyFTg1l3K0aTH0uX6PzgaLfzJBK&index=1
     */
    for (var i = 0; i < instanceData.length; i++) {

        var olderThan30Days = isOlderThanXDays(30, instanceData[i].date_launched);
        if (olderThan30Days) {
            var row = `<tr>
                            <td> ${instanceData[i].instance_id}</td>
                            <td> ${instanceData[i].ami_id}</td>
                            <td bgcolor="#f59396"> ${instanceData[i].date_launched}</td>
                            </tr>`
            table.innerHTML += row;
        } else {
            var row = `<tr>
                            <td> ${instanceData[i].instance_id}</td>
                            <td> ${instanceData[i].ami_id}</td>
                            <td  bgcolor="#a4dbb2"> ${instanceData[i].date_launched}</td>
                            </tr>`
            table.innerHTML += row;
        }
    }

}


function buildCustomImagesTable(AMIData) {
    var table = document.getElementById('AMIsTable');
    table.innerHTML = '';

    /**
     * "for" loop adapted from Dennis Ivy (2019) JSON Array to HTML Table with Javascript
     * Available at https://www.youtube.com/watch?v=XmdOZ5NSqb8&list=PL-51WBLyFTg1l3K0aTH0uX6PzgaLfzJBK&index=1
     */
    for (var i = 0; i < AMIData.length; i++) {
        var olderThan30Days = isOlderThanXDays(30, AMIData[i].creation_date);

        if (olderThan30Days){
            var row = `<tr>
                            <td> ${AMIData[i].image_id}</td>
                            <td> ${AMIData[i].image_name}</td>
                            <td bgcolor="#f59396"> ${AMIData[i].creation_date}</td>
                            </tr>`
            table.innerHTML += row;
        } else {
            var row = `<tr>
                            <td> ${AMIData[i].image_id}</td>
                            <td> ${AMIData[i].image_name}</td>
                            <td bgcolor="#a4dbb2"> ${AMIData[i].creation_date}</td>
                            </tr>`
            table.innerHTML += row;
        }


    }
}

function searchInstancesTable(searchValue, data){
    var filteredData = []
    for (var i = 0; i < data.length; i++) {
        searchValue = searchValue.toLowerCase(); // No case sensitivity
        var instance_id = data[i].instance_id.toLowerCase()
        var ami_id = data[i].ami_id.toLowerCase()

        if (instance_id.includes(searchValue)){
            filteredData.push(data[i])
        }
        else if (ami_id.includes(searchValue)){
            filteredData.push(data[i])
        }
    }
    return filteredData
}

function searchImagesTable(searchValue, data){
    var filteredData = [];
    for (var i = 0; i < data.length; i++) {
        searchValue = searchValue.toLowerCase(); // No case sensitivity
        var imageID = data[i].image_id.toLowerCase();

        if (imageID.includes(searchValue)){
            filteredData.push(data[i])
        }
    }
    return filteredData;
}

