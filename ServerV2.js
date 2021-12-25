//Load express module
const express = require('express');
const path = require('path');
const axios = require('axios');
//Put new Express application inside app variable
const app = express();
const bodyParser  = require('body-parser');
const { response } = require('express');
app.use(bodyParser.urlencoded());

//Set views property and view engine
app.set("views", path.resolve(__dirname, "views"));
app.set("view engine", "ejs");

const port = 8080;

app.get('/',function(req,res)
{
    res.render("Main")
})

//Main Page

app.get('/Main',function(req,res)
{
    res.render("Main")
})
app.post('/Main',function(req,res)
{
    res.render("Main")
})

app.post('/Main',function(req,res)
{
    res.render("Main")
})


app.get('/Customer/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Customer/') 
    .then((response) => {
     var Customer = response.data;
     console.log(Customer)
    res.render('Customer', {
        Customer: Customer
    })
    })
})

app.get('/Customer/add',function(req, res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Country/') 
    .then((response) => {
     var Country = response.data;
     console.log(Country)
     axios.get('http://127.0.0.1:5000/State/') 
     .then((response) => {
      var State = response.data;
    res.render('AddCustomer', {
        Country: Country,
        State:State
    })
    })
    })  
])
})

app.post('/Customer/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Customer/add', { 
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        CustomerHomeNumber: req.body.CustomerHomeNumber,
        CustomerCellNumber: req.body.CustomerCellNumber,
        State: req.body.State,
        Country: req.body.Country
    })
    return res.redirect('/Customer')
})

app.get('/Customer/update/:id',function(req,res)
{
    axios.all([
        axios.get('http://127.0.0.1:5000/Customer/update/' + req.params.id)
        .then((response) => {
        var Customer = response.data;
    axios.get('http://127.0.0.1:5000/CustomerStatus/')
    .then((response) => {
        var CustomerStatus = response.data;
    axios.get('http://127.0.0.1:5000/Country/')
    .then((response) => {
        var Country = response.data;
    axios.get('http://127.0.0.1:5000/State/')
    .then((response) => {
        var State = response.data;
    res.render('UpdateCustomer',{
        Customer: Customer,
        CustomerStatus: CustomerStatus,
        Country : Country,
        State : State,
        id: req.params.id
    })
    })
    })
    })
    })
    ])  
})

app.post('/Customer/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Customer/update/' + req.params.id, {
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        CustomerHomeNumber: req.body.CustomerHomeNumber,
        CustomerCellNumber: req.body.CustomerCellNumber,
        State: req.body.State,
        Country: req.body.Country,
        Status: req.body.Status,
        CustomerStrike: req.body.CustomerStrike,
        StrikeComment: req.body.StrikeComment,
    

    })
    return res.redirect('/Customer')
})


app.get('/Customer/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Customer/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Customer')
})


app.get('/Appointment/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Appointment/') 
    .then((response) => {
     var Appointment = response.data;
     console.log(Appointment)
    res.render('Appointment', {
        Appointment: Appointment
    })
    })
})

app.get('/Appointment/add',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Service/') 
    .then((response) => {
     var Service = response.data;
     console.log(Service)
    res.render('AddAppointment', {
        Service: Service
    })
    })
})
app.post('/Appointment/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Appointment/add', { 
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        AppointmentDate: req.body.AppointmentDate,
        AppointmentTime: req.body.AppointmentTime,
        ServiceName: req.body.ServiceName
    })
    return res.redirect('/Appointment')
})

app.get('/Appointment/update/:id',function(req,res)
{
    
    axios.get('http://127.0.0.1:5000/Appointment/update/' + req.params.id)
    .then((response) => {
     var Appointment = response.data;
    res.render('UpdateAppointment',{
        Appointment: Appointment,
        id: req.params.id
    })
    })
})


app.post('/Appointment/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Appointment/update/' + req.params.id, {
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        AppointmentDate: req.body.AppointmentDate,
        AppointmentTime: req.body.AppointmentTime,
        ServiceName: req.body.ServiceName
    })
    return res.redirect('/Appointment')
})


app.get('/Appointment/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Appointment/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Appointment')
})

app.get('/AppointmentService/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/AppointmentService/') 
    .then((response) => {
     var AppointmentService = response.data;
     console.log(AppointmentService)
    res.render('AppointmentService', {
        AppointmentService: AppointmentService
    })
    })
})

app.get('/AppointmentService/add',function(req, res)
{
    res.render('AddAppointmentService')
})
app.post('/AppointmentService/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/AppointmentService/add', { 
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        AppointmentDate: req.body.AppointmentDate,
        ServiceName: req.body.ServiceName
    })
    return res.redirect('/AppointmentService')
})

app.get('/AppointmentService/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/AppointmentService/update/' + req.params.id)
    .then((response) => {
     var AppointmentService = response.data;
    res.render('UpdateAppointmentService',{
        AppointmentService: AppointmentService,
        id: req.params.id
    })
    })
})
app.post('/AppointmentService/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/AppointmentService/update/' + req.params.id, {
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        AppointmentDate: req.body.AppointmentDate,
        ServiceName: req.body.ServiceName
    })
    return res.redirect('/AppointmentService')
})

app.get('/AppointmentService/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/AppointmentService/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/AppointmentService')
})

app.get('/AcquiredSkill/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/AcquiredSkill/') 
    .then((response) => {
     var AcquiredSkill = response.data;
     console.log(AcquiredSkill)
    res.render('AcquiredSkill', {
        AcquiredSkill: AcquiredSkill
    })
    })
})


app.get('/AcquiredSkill/add',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Skill/') 
    .then((response) => {
     var Skill = response.data;
     console.log(Skill)
    res.render('AddAcquiredSkill', {
        Skill: Skill
    })
    })
})
app.post('/AcquiredSkill/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/AcquiredSkill/add', { 
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        SkillName: req.body.SkillName,
        DateAcq: req.body.DateAcq,
        AcqSkillInstitution: req.body.AcqSkillInstitution,
        AcqSkillState: req.body.AcqSkillState
    })
    return res.redirect('/AcquiredSkill')
})

app.get('/AcquiredSkill/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/AcquiredSkill/update/' + req.params.id)
    .then((response) => {
     var AcquiredSkill = response.data;
     axios.get('http://127.0.0.1:5000/Skill/') 
     .then((response) => {
      var Skill = response.data;
      console.log(Skill)
    res.render('UpdateAcquiredSkill',{
        AcquiredSkill: AcquiredSkill,
        Skill:Skill,
        id: req.params.id
    })
    })
})
])
})
app.post('/AcquiredSkill/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/AcquiredSkill/update/' + req.params.id, {
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        SkillName: req.body.SkillName,
        DateAcq: req.body.DateAcq,
        AcqSkillInstitution: req.body.AcqSkillInstitution,
        AcqSkillState: req.body.AcqSkillState
    })
    return res.redirect('/AcquiredSkill')
})


app.get('/AcquiredSkill/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/AcquiredSkill/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/AcquiredSkill')
})

app.get('/RequiredSkill/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/RequiredSkill/') 
    .then((response) => {
     var RequiredSkill = response.data;
     console.log(RequiredSkill)
    res.render('RequiredSkill', {
        RequiredSkill: RequiredSkill
        
    })
    }) 
})

app.get('/RequiredSkill/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Skill/') 
    .then((response) => {
     var Skill = response.data;
     console.log(Skill)
     axios.get('http://127.0.0.1:5000/Service/') 
     .then((response) => {
      var Service = response.data;
    res.render('AddRequiredSkill', {
        Skill: Skill,
        Service:Service
        
    })
    }) 
})
])  
})

app.post('/RequiredSkill/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/RequiredSkill/add', { 
        ServiceName: req.body.ServiceName,
        SkillName: req.body.SkillName
    })
    return res.redirect('/RequiredSkill')
})

app.get('/RequiredSkill/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/RequiredSkill/update/' + req.params.id)
    .then((response) => {
     var RequiredSkill = response.data;
     axios.get('http://127.0.0.1:5000/Skill/') 
     .then((response) => {
      var Skill = response.data;
      console.log(Skill)
      axios.get('http://127.0.0.1:5000/Service/') 
      .then((response) => {
       var Service = response.data;
    res.render('UpdateRequiredSkill',{
        RequiredSkill: RequiredSkill,
        Skill: Skill,
        Service:Service,
        id: req.params.id
    })
    })
    })
    })  
    ])
})
app.post('/RequiredSkill/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/RequiredSkill/update/' + req.params.id, {
        ServiceName: req.body.ServiceName,
        SkillName: req.body.SkillName
    })
    return res.redirect('/RequiredSkill')
})

app.get('/RequiredSkill/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/RequiredSkill/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/RequiredSkill')
})

app.get('/EmployeeRole/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeRole/') 
    .then((response) => {
     var EmployeeRole = response.data;
     console.log(EmployeeRole)
    res.render('EmployeeRole', {
        EmployeeRole: EmployeeRole
    })
    }) 
})

app.get('/EmployeeRole/add',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Role/') 
    .then((response) => {
     var Role = response.data;
     console.log(Role)
    res.render('AddEmployeeRole', {
        Role: Role
    })
    }) 
})
app.post('/EmployeeRole/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/EmployeeRole/add', { 
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        RoleTitle:req.body.RoleTitle,
        YearofRole:req.body.YearofRole
    })
    return res.redirect('/EmployeeRole')
})

app.get('/EmployeeRole/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeRole/update/' + req.params.id)
    .then((response) => {
     var EmployeeRole = response.data;
    res.render('UpdateEmployeeRole',{
        EmployeeRole: EmployeeRole,
        id: req.params.id
    })
    })
})
app.post('/EmployeeRole/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/EmployeeRole/update/' + req.params.id, {
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        RoleTitle:req.body.RoleTitle,
        YearofRole:req.body.YearofRole
    })
    return res.redirect('/EmployeeRole')
})

app.get('/EmployeeRole/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/EmployeeRole/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/EmployeeRole')
})

app.get('/Satisfaction/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Satisfaction/') 
    .then((response) => {
     var Satisfaction = response.data;
     console.log(Satisfaction)
    res.render('Satisfaction', {
        Satisfaction: Satisfaction
    })
    }) 
})

app.get('/Satisfaction/add',function(req,res)
{
    axios.get('http://127.0.0.1:5000/SatisfactionMeaning/') 
    .then((response) => {
     var SatisfactionMeaning = response.data;
     console.log(SatisfactionMeaning)
    res.render('AddSatisfaction', {
        SatisfactionMeaning: SatisfactionMeaning
    })
    })   
})
app.post('/Satisfaction/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Satisfaction/add', { 
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        AppointmentDate: req.body.AppointmentDate,
        AppointmentSatisfaction: req.body.AppointmentSatisfaction,
        Comments:req.body.Comments
    })
    return res.redirect('/Satisfaction')
})


app.get('/Satisfaction/update/:id',function(req,res)
{
    axios.all([
        axios.get('http://127.0.0.1:5000/Satisfaction/update/' + req.params.id)
            .then((response) => {
            var Satisfaction = response.data;
        axios.get('http://127.0.0.1:5000/SatisfactionMeaning/')
        .then((response) => {
            var SatisfactionMeaning = response.data;
        res.render('UpdateSatisfaction',{
            Satisfaction: Satisfaction,
            SatisfactionMeaning: SatisfactionMeaning,
            id: req.params.id
    })
    })
    })
    ])
})
app.post('/Satisfaction/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Satisfaction/update/' + req.params.id, {
        CustomerFirstName: req.body.CustomerFirstName,
        CustomerLastName: req.body.CustomerLastName,
        AppointmentDate: req.body.AppointmentDate,
        AppointmentSatisfaction: req.body.AppointmentSatisfaction,
        Comments:req.body.Comments
    })
    return res.redirect('/Satisfaction')
})

app.get('/Satisfaction/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Satisfaction/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Satisfaction')
})


app.get('/Employee',function(req,res)
{ 
    axios.get('http://127.0.0.1:5000/Employee/') 
    .then((response) => {
     var Employee = response.data;
     console.log(Employee)
    res.render('Employee', {
        Employee:Employee

    }) 
    })  
})

app.get('/Employee/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Employee/') 
    .then((response) => {
     var Employee = response.data;
     console.log(Employee)
    axios.get('http://127.0.0.1:5000/EmployeeStatus/')
    .then((response) => {
        var EmployeeStatus = response.data;
    axios.get('http://127.0.0.1:5000/Country/')
    .then((response) => {
        var Country = response.data;
    axios.get('http://127.0.0.1:5000/State/')
    .then((response) => {
        var State = response.data;
    axios.get('http://127.0.0.1:5000/EmployeeRank/')
    .then((response) => {
        var EmployeeRank = response.data;
    res.render('AddEmployee', {
        EmployeeStatus:EmployeeStatus,
        Employee:Employee,
        Country:Country,
        State:State,
        EmployeeRank:EmployeeRank

    }) 
    }) 
    })
    })
    })
})
]) 
})

app.post('/Employee/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/Employee/add', { 
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        RankTitle: req.body.RankTitle,
        EmployeeHomeNumber: req.body.EmployeeHomeNumber,
        EmployeeCellNumber: req.body.EmployeeCellNumber,
        Country: req.body.Country,
        State: req.body.State,
        EmployeeStreetName: req.body.EmployeeStreetName,
        EmployeeCity: req.body.EmployeeCity,
        EmployeeZipCode: req.body.EmployeeZipCode,
        HireDate: req.body.HireDate,
        EmployeeStatus: req.body.EmployeeStatus
        
        
    })
    return res.redirect('/Employee')
})   

app.get('/Employee/update/:id',function(req,res)
{
    axios.all([
        axios.get('http://127.0.0.1:5000/Employee/update/' + req.params.id) 
        .then((response) => {
         var Employee = response.data;
         console.log(Employee)
        axios.get('http://127.0.0.1:5000/EmployeeStatus/')
        .then((response) => {
            var EmployeeStatus = response.data;
        axios.get('http://127.0.0.1:5000/Country/')
        .then((response) => {
            var Country = response.data;
        axios.get('http://127.0.0.1:5000/State/')
        .then((response) => {
            var State = response.data;
        axios.get('http://127.0.0.1:5000/EmployeeRank/')
        .then((response) => {
            var EmployeeRank = response.data;
        res.render('UpdateEmployee', {
            EmployeeStatus:EmployeeStatus,
            Employee:Employee,
            Country:Country,
            State:State,
            EmployeeRank:EmployeeRank,
            id: req.params.id
    
      
    })
    })
    })
    })
    })
    })
    ])
})
app.post('/Employee/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Employee/update/' + req.params.id, {
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        RankTitle: req.body.RankTitle,
        EmployeeHomeNumber: req.body.EmployeeHomeNumber,
        EmployeeCellNumber: req.body.EmployeeCellNumber,
        Country: req.body.Country,
        State: req.body.State,
        EmployeeStreetName: req.body.EmployeeStreetName,
        EmployeeCity: req.body.EmployeeCity,
        EmployeeZipCode: req.body.EmployeeZipCode,
        HireDate: req.body.HireDate,
        EmployeeStatus: req.body.EmployeeStatus
    })
    return res.redirect('/Employee')
})

app.get('/Employee/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Employee/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Employee')
})



app.get('/EmployeeTimeOff/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeTimeOff/') 
    .then((response) => {
     var EmployeeTimeOff = response.data;
     console.log(EmployeeTimeOff)
    res.render('EmployeeTimeOff', {
        EmployeeTimeOff: EmployeeTimeOff
    })
    })
})
app.get('/EmployeeTimeOff/add',function(req,res)
{
    res.render('AddEmployeeTimeOff')    
})

app.post('/EmployeeTimeOff/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/EmployeeTimeOff/add', { 
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        StartTimeOffDate: req.body.StartTimeOffDate,
        AvailabilityDate: req.body.AvailabilityDate,
        Reason: req.body.Reason
    })
    return res.redirect('/EmployeeTimeOff')
})   

app.get('/EmployeeTimeOff/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeTimeOff/update/' + req.params.id)
    .then((response) => {
     var EmployeeTimeOff = response.data;
    res.render('UpdateEmployeeTimeOff',{
        EmployeeTimeOff: EmployeeTimeOff,
        id: req.params.id
    })
    })
})
app.post('/EmployeeTimeOff/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/EmployeeTimeOff/update/' + req.params.id, {
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        StartTimeOffDate: req.body.StartTimeOffDate,
        AvailabilityDate: req.body.AvailabilityDate,
        Reason: req.body.Reason
    })
    return res.redirect('/EmployeeTimeOff')
})

app.get('/EmployeeTimeOff/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/EmployeeTimeOff/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/EmployeeTimeOff')
})

app.get('/EmployeeSchedule/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeSchedule/') 
    .then((response) => {
     var EmployeeSchedule = response.data;
     console.log(EmployeeSchedule)
    res.render('EmployeeSchedule', {
        EmployeeSchedule: EmployeeSchedule
    })
    })
})

app.get('/EmployeeSchedule/add',function(req,res)
{
    res.render('AddEmployeeSchedule')    
})

app.post('/EmployeeSchedule/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/EmployeeSchedule/add', { 
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        ClockIn: req.body.ClockIn,
        ClockOut: req.body.ClockOut,
        DayofWeek: req.body.DayofWeek
    })
    return res.redirect('/EmployeeSchedule')
})   


app.get('/EmployeeSchedule/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeSchedule/update/' + req.params.id)
    .then((response) => {
     var EmployeeSchedule = response.data;
     console.log(EmployeeSchedule)
    res.render('UpdateEmployeeSchedule', {
        EmployeeSchedule: EmployeeSchedule,
        id: req.params.id
    })
    })
})

app.post('/EmployeeSchedule/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/EmployeeSchedule/update' + req.params.id, { 
        EmployeeFirstName: req.body.EmployeeFirstName,
        EmployeeLastName: req.body.EmployeeLastName,
        ClockIn: req.body.ClockIn,
        ClockOut: req.body.ClockOut,
        DayofWeek: req.body.DayofWeek
    })
    return res.redirect('/EmployeeSchedule')
})   

app.get('/EmployeeSchedule/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/EmployeeSchedule/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/EmployeeSchedule')
})
app.get('/ServiceInclusion/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/ServiceInclusion/') 
    .then((response) => {
     var ServiceInclusion = response.data;
     console.log(ServiceInclusion)
    res.render('ServiceInclusion', {
        ServiceInclusion: ServiceInclusion
    })
    })
})

app.get('/ServiceInclusion/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Inclusion/') 
    .then((response) => {
     var Inclusion = response.data;
     console.log(Inclusion)
    axios.get('http://127.0.0.1:5000/Service/') 
    .then((response) => {
    var Service = response.data;
    res.render('AddServiceInclusion', {
        Inclusion: Inclusion,
        Service:Service
    })
    })   

})
])
})

app.post('/ServiceInclusion/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/ServiceInclusion/add', { 
        ServiceName: req.body.ServiceName,
        InclusionName: req.body.InclusionName
    })
    return res.redirect('/ServiceInclusion')
})   
app.get('/ServiceInclusion/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/ServiceInclusion/update/' + req.params.id)
    .then((response) => {
     var ServiceInclusion = response.data;
     console.log(ServiceInclusion)
     axios.get('http://127.0.0.1:5000/Inclusion/') 
     .then((response) => {
      var Inclusion = response.data;
      console.log(Inclusion)
     axios.get('http://127.0.0.1:5000/Service/') 
     .then((response) => {
     var Service = response.data;
    res.render('UpdateServiceInclusion', {
        ServiceInclusion: ServiceInclusion,
        Inclusion: Inclusion,
        Service:Service,
        id: req.params.id
    })
    })
    })
    })
])
})
app.post('/ServiceInclusion/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/ServiceInclusion/update' + req.params.id, { 
        ServiceName: req.body.ServiceName,
        InclusionName: req.body.InclusionName
    })
    return res.redirect('/ServiceInclusion')
})   

app.get('/ServiceInclusion/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/ServiceInclusion/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/ServiceInclusion')
})

app.get('/ServiceTool/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/ServiceTool/') 
    .then((response) => {
     var ServiceTool = response.data;
     console.log(ServiceTool)
    res.render('ServiceTool', {
        ServiceTool: ServiceTool
    })
    })
})

app.get('/ServiceTool/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Tool/') 
    .then((response) => {
     var Tool = response.data;
     console.log(Tool)
     axios.get('http://127.0.0.1:5000/Service/') 
     .then((response) => {
      var Service = response.data;
    res.render('AddServiceTool', {
        Tool: Tool,
        Service:Service
    })
    })
    })
    ])
})

app.post('/ServiceTool/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/ServiceTool/add', { 
        ToolName: req.body.ToolName,
        ServiceName: req.body.ServiceName,
        Quantity: req.body.Quantity,
        Unit: req.body.Unit
    })
    return res.redirect('/ServiceTool')
})   

app.get('/ServiceTool/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/ServiceTool/update/' + req.params.id)
    .then((response) => {
     var ServiceTool = response.data;
     console.log(ServiceTool)
     axios.get('http://127.0.0.1:5000/Tool/') 
    .then((response) => {
     var Tool = response.data;
     console.log(Tool)
     axios.get('http://127.0.0.1:5000/Service/') 
     .then((response) => {
      var Service = response.data;
    res.render('UpdateServiceTool', {
        ServiceTool: ServiceTool,
        Tool: Tool,
        Service:Service,
        id: req.params.id
    })
    })
    })
    })
    ])
})
app.post('/ServiceTool/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/ServiceTool/update/' + req.params.id, { 
        ToolName: req.body.ToolName,
        ServiceName: req.body.ServiceName,
        Quantity: req.body.Quantity,
        Unit: req.body.Unit
    })
    return res.redirect('/ServiceTool')
})   

app.get('/ServiceTool/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/ServiceTool/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/ServiceTool')
})


app.get('/ToolManufacturer/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/ToolManufacturer/') 
    .then((response) => {
     var ToolManufacturer = response.data;
     console.log(ToolManufacturer)
    res.render('ToolManufacturer', {
        ToolManufacturer: ToolManufacturer
    })
    })
})

app.get('/ToolManufacturer/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Tool/') 
    .then((response) => {
     var Tool = response.data;
     axios.get('http://127.0.0.1:5000/Manufacturer/') 
     .then((response) => {
      var Manufacturer = response.data;
     console.log(Manufacturer)
    res.render('AddToolManufacturer', {
        Tool: Tool,
        Manufacturer: Manufacturer
    })
    })  
}) 
])
})

app.post('/ToolManufacturer/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/ToolManufacturer/add', { 
        ManufacturerName: req.body.ManufacturerName,
        ToolName: req.body.ToolName,
        ToolManufacturerName: req.body.ToolManufacturerName
    })
    return res.redirect('/ToolManufacturer')
})   

app.get('/ToolManufacturer/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/ToolManufacturer/update/' + req.params.id)
    .then((response) => {
     var ToolManufacturer = response.data;
     console.log(ToolManufacturer)
     axios.get('http://127.0.0.1:5000/Tool/') 
     .then((response) => {
      var Tool = response.data;
      axios.get('http://127.0.0.1:5000/Manufacturer/') 
      .then((response) => {
       var Manufacturer = response.data;
    res.render('UpdateToolManufacturer', {
        ToolManufacturer: ToolManufacturer,
        Tool: Tool,
        Manufacturer: Manufacturer,
        id: req.params.id
    })
    })
    })
    })
])
})

app.post('/ToolManufacturer/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/ToolManufacturer/update/' + req.params.id, { 
        ManufacturerName: req.body.ManufacturerName,
        ToolName: req.body.ToolName,
        ToolManufacturerName: req.body.ToolManufacturerName
    })
    return res.redirect('/ToolManufacturer')
})   

app.get('/ToolManufacturer/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/ToolManufacturer/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/ToolManufacturer')
})

app.get('/HairServiceProduct/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/HairServiceProduct/') 
    .then((response) => {
     var HairServiceProduct = response.data;
     console.log(HairServiceProduct)
    res.render('HairServiceProduct', {
        HairServiceProduct: HairServiceProduct
    })
    })
})

app.get('/HairServiceProduct/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/HairProduct/') 
    .then((response) => {
     var Product = response.data;
     console.log(Product)
     axios.get('http://127.0.0.1:5000/Service/') 
     .then((response) => {
      var Service = response.data;
    res.render('AddHAirServiceProduct', {
        Product: Product,
        Service:Service
    })
    })
    })
    ])
})

app.post('/HairServiceProduct/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/HairServiceProduct/add', { 
        ProductName: req.body.ProductName,
        ServiceName: req.body.ServiceName,
        QuantityUsed: req.body.QuantityUsed,
        ProductVolume: req.body.ProductVolume
    })
    return res.redirect('/HairServiceProduct')
})  

app.get('/HairServiceProduct/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/HairServiceProduct/update/' + req.params.id)
    .then((response) => {
     var HairServiceProduct = response.data;
     console.log(HairServiceProduct)
     axios.get('http://127.0.0.1:5000/HairProduct/') 
     .then((response) => {
      var Product = response.data;
      console.log(Product)
      axios.get('http://127.0.0.1:5000/Service/') 
      .then((response) => {
       var Service = response.data;
    res.render('UpdateHairServiceProduct', {
        HairServiceProduct: HairServiceProduct,
        Product: Product,
        Service:Service,
        id: req.params.id
    })
    })
    })
    })
])
})

app.post('/HairServiceProduct/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/HairServiceProduct/update/' + req.params.id, { 
        ProductName: req.body.ProductName,
        ServiceName: req.body.ServiceName,
        QuantityUsed: req.body.QuantityUsed,
        ProductVolume: req.body.ProductVolume
    })
    return res.redirect('/HairServiceProduct')
})   

app.get('/HairServiceProduct/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/HairServiceProduct/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/HairServiceProduct')
})

app.get('/HairProductManufacturer/',function(req,res)
{
    axios.get('http://127.0.0.1:5000/HairProductManufacturer/') 
    .then((response) => {
     var HairProductManufacturer = response.data;
     console.log(HairProductManufacturer)
    res.render('HairProductManufacturer', {
        HairProductManufacturer: HairProductManufacturer
    })
    })
})

app.get('/HairProductManufacturer/add',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/HairProduct/') 
    .then((response) => {
     var Product = response.data;
     console.log(Product)
     axios.get('http://127.0.0.1:5000/Manufacturer/') 
     .then((response) => {
      var Manufacturer = response.data;
      console.log(Manufacturer)
    res.render('AddHairProductManufacturer', {
        Product: Product,
        Manufacturer: Manufacturer
    })
    }) 
})
])
})

app.post('/HairProductManufacturer/add',function(req,res)
{
    axios.post('http://127.0.0.1:5000/HairProductManufacturer/add', { 
        ProductName: req.body.ProductName,
        ManufacturerName: req.body.ManufacturerName,
        HairProductManufacturerName: req.body.HairProductManufacturerName
    })
    return res.redirect('/HairProductManufacturer')
})  

app.get('/HairProductManufacturer/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/HairProductManufacturer/update/' + req.params.id)
    .then((response) => {
     var HairProductManufacturer = response.data;
     console.log(HairProductManufacturer)
     axios.get('http://127.0.0.1:5000/HairProduct/') 
     .then((response) => {
      var Product = response.data;
      console.log(Product)
      axios.get('http://127.0.0.1:5000/Manufacturer/') 
      .then((response) => {
       var Manufacturer = response.data;
    res.render('UpdateHairProductManufacturer', {
        HairProductManufacturer: HairProductManufacturer,
        Product: Product,
        Manufacturer: Manufacturer,
        id: req.params.id
    })
    })
    })
    })
])
})

app.post('/HairProductManufacturer/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/HairProductManufacturer/update/' + req.params.id, { 
        ProductName: req.body.ProductName,
        ManufacturerName: req.body.ManufacturerName,
        HairProductManufacturerName: req.body.HairProductManufacturerName
    })
    return res.redirect('/HairProductManufacturer')
})   

app.get('/HairProductManufacturer/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/HairProductManufacturer/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/HairProductManufacturer')
})

app.get('/EmployeeStatus/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/EmployeeStatus/') 
    .then((response) => {
     var EmployeeStatus = response.data;
     console.log(EmployeeStatus)
    res.render('EmployeeStatus', {
        EmployeeStatus: EmployeeStatus
    })
    })
})



app.get('/EmployeeStatus/add',function(req, res)
{
    res.render('AddEmployeeStatus')
})

app.post('/EmployeeStatus/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/EmployeeStatus/add', { 
        EmployeeStatusID: req.body.EmployeeStatusID,
        StatusDescription: req.body.StatusDescription

    })
    return res.redirect('/EmployeeStatus')
})



app.get('/EmployeeStatus/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Employee/')
    .then((response) => {
     var EmployeeStatus = response.data;
    res.render('UpdateEmployeeStatus',{
        EmployeeStatus: EmployeeStatus,
        id: req.params.id
    })
    })
})

app.post('/EmployeeStatus/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/EmployeeStatus/update/' + req.params.id, {
        EmployeeStatusID: req.body.EmployeeStatusID,
        StatusDescription: req.body.StatusDescription

    })
    return res.redirect('/EmployeeStatus')
})


app.get('/EmployeeStatus/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/EmployeeStatus/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/EmployeeStatus')
})


app.get('/CustomerStatus/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/CustomerStatus/') 
    .then((response) => {
     var CustomerStatus = response.data;
     console.log(CustomerStatus)
    res.render('CustomerStatus', {
        CustomerStatus: CustomerStatus
    })
    })
})



app.get('/CustomerStatus/add',function(req, res)
{
    res.render('AddCustomerStatus')
})

app.post('/CustomerStatus/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/CustomerStatus/add', { 
        CustomerStatusID: req.body.CustomerStatusID,
        StatusDescription: req.body.StatusDescription
    })
    return res.redirect('/CustomerStatus')
})



app.get('/CustomerStatus/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/CustomerStatus/')
    .then((response) => {
     var CustomerStatus = response.data;
    res.render('UpdateCustomerStatus',{
        CustomerStatus: CustomerStatus,
        id: req.params.id
    })
    })
})

app.post('/CustomerStatus/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/CustomerStatus/update/' + req.params.id, {
        CustomerStatusID: req.body.CustomerStatusID,
        StatusDescription: req.body.StatusDescription
    })
    return res.redirect('/CustomerStatus')
})


app.get('/CustomerStatus/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/CustomerStatus/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/CustomerStatus')
})




app.get('/BusinessHours/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/BusinessHours/') 
    .then((response) => {
     var DaysofOperation = response.data;
     console.log(DaysofOperation)
    res.render('DaysofOperation', {
        DaysofOperation: DaysofOperation
    })
    })
})



app.get('/BusinessHours/add',function(req, res)
{
    res.render('AddDayOfOperation')
})

app.post('/BusinessHours/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/BusinessHours/add', { 
        DaysofOperationsID: req.body.DaysofOperationID,
        DayName: req.body.DayName,
        IsActive: req.body.IsActive
    })
    return res.redirect('/BusinessHours')
})



app.get('/BusinessHours/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/BusinessHours/')
    .then((response) => {
     var DaysofOperation = response.data;
    res.render('UpdateDayOfOperation',{
        DaysofOperation: DaysofOperation,
        id: req.params.id
    })
    })
})

app.post('/BusinessHours/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/BusinessHours/update/' + req.params.id, {
        DaysofOperationsID: req.body.DaysofOperationID,
        DayName: req.body.DayName,
        IsActive: req.body.IsActive

    })
    return res.redirect('/BusinessHours')
})


app.get('/BusinessHours/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/BusinessHours/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/BusinessHours')
})


app.get('/Tool/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Tool/') 
    .then((response) => {
     var Tool = response.data;
     console.log(Tool)
    res.render('Tool', {
        Tool: Tool
    })
    })
})



app.get('/Tool/add',function(req, res)
{
    res.render(' AddTool')
})

app.post('/Tool/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Tool/add', { 
        ToolID: req.body.ToolID,
        ToolName: req.body.ToolName,
        ToolDescription: req.body.ToolDescription
    })
    return res.redirect('/Tool')
})



app.get('/Tool/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Tool/')
    .then((response) => {
     var Tool = response.data;
    res.render('UpdateTool',{
        Tool: Tool,
        id: req.params.id
    })
    })
})

app.post('/Tool/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Tool/update/' + req.params.id, {
        ToolID: req.body.ToolID,
        ToolName: req.body.ToolName,
        ToolDescription: req.body.ToolDescription


    })
    return res.redirect('/Tool')
})

app.get('/Tool/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Tool/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Tool')
})
/*
app.get('/HairProduct/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/HairProduct/') 
    .then((response) => {
     var HairProduct = response.data;
     console.log(HairProduct)
    res.render('HairProduct', {
        HairProduct: HairProduct
    })
    })
})

app.post('/HairProduct/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/HairProduct/add', { 
        ProductType: req.body.ProductType,
        ProductName: req.body.ProductName,
        ProductDescription: req.body.ProductDescription,
        ProductVolume: req.body.ProductVolume,
    })
    return res.redirect('/HairProduct')
})

app.get('/HairProduct/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/HairProduct/update/' + req.params.id)
    .then((response) => {
     var HairProduct = response.data;
    res.render('UpdateHairProduct',{
        HairProduct: HairProduct,
        id: req.params.id
    })
    })
})

app.post('/HairProduct/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/HairProduct/update/' + req.params.id, {
        ProductType: req.body.ProductType,
        ProductName: req.body.ProductName,
        ProductDescription: req.body.ProductDescription,
        ProductVolume: req.body.ProductVolume,
    })
    return res.redirect('/HairProduct')
})
*/
//COUNTRY

app.get('/Country/add',function(req, res)
{
    res.render('AddCountry')
}) 

app.get('/Country/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Country/') 
    .then((response) => {
     var Country = response.data;
     console.log(Country)
    res.render('Country', {
        Country: Country
    })
    })
})

app.post('/Country/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Country/add', { 
        CountryCode: req.body.CountryCode,
        CountryInitial: req.body.CountryInitial,
        CountryName: req.body.CountryName,
    })
    return res.redirect('/Country')
})

app.get('/Country/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Country/update/' + req.params.id)
    .then((response) => {
     var Country = response.data;
    res.render('UpdateCountry',{
        Country: Country,
        id: req.params.id
    })
    })
})

app.post('/Country/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Country/update/' + req.params.id, {
        CountryCode: req.body.CountryCode,
        CountryInitial: req.body.CountryInitial,
        CountryName: req.body.CountryName,
    })
    return res.redirect('/Country')
})
app.get('/Country/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Country/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Country')
})

//STATE

app.get('/State/add',function(req, res)
{
    res.render('AddState')
}) 

app.get('/State/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/State/') 
    .then((response) => {
     var State = response.data;
     console.log()
    res.render('State', {
        State: State
    })
    })
})

app.post('/State/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/State/add', {
        StateInitial: req.body.StateInitial,
        StateName: req.body.StateName,
    })
    return res.redirect('/State')
})

app.get('/State/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/State/update/' + req.params.id)
    .then((response) => {
     var State = response.data;
    res.render('UpdateState',{
        State: State,
        id: req.params.id
    })
    })
})

app.post('/State/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/State/update/' + req.params.id, {
        StateInitial: req.body.StateInitial,
        StateName: req.body.StateName,
    })
    return res.redirect('/State')
})

app.get('/State/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/State/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/State')
})

//MANUFACTURER

app.get('/Manufacturer/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Manufacturer/') 
    .then((response) => {
     var Manufacturer = response.data;
    res.render('Manufacturer', {
        Manufacturer: Manufacturer
    })
    })
})

app.get('/Manufacturer/add',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Country/') 
    .then((response) => {
     var Country = response.data;
    res.render('AddManufacturer', {
        Country: Country
    })
    })
}) 

app.post('/Manufacturer/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Manufacturer/add', {
        ManufacturerName: req.body.ManufacturerName,
        Country: req.body.Country,
        ManufacturerPhoneNumber: req.body.ManufacturerPhoneNumber,
        ManufacturerEmail: req.body.ManufacturerEmail,
    })
    return res.redirect('/Manufacturer')
})

app.get('/Manufacturer/update/:id',function(req,res)
{
    axios.all([
    axios.get('http://127.0.0.1:5000/Manufacturer/update/' + req.params.id)
    .then((response) => {
     var Manufacturer = response.data;
    axios.get('http://127.0.0.1:5000/Country/') 
     .then((response) => {
      var Country = response.data;
    res.render('UpdateManufacturer',{
        Manufacturer: Manufacturer,
        Country: Country,
        id: req.params.id
    })
    })
})
])
})


app.post('/Manufacturer/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Manufacturer/update/' + req.params.id, {
        ManufacturerName: req.body.ManufacturerName,
        CountryID: req.body.CountryID,
        ManufacturerPhoneNumber: req.body.ManufacturerPhoneNumber,
        ManufacturerEmail: req.body.ManufacturerEmail,
    })
    return res.redirect('/Manufacturer')
})

app.get('/Manufacturer/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Manufacturer/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Manufacturer')
})

//EMPLOYEE RANK

app.get('/EmployeeRank/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/EmployeeRank/') 
    .then((response) => {
     var EmployeeRank = response.data;
     console.log()
    res.render('EmployeeRank', {
        EmployeeRank: EmployeeRank
    })
    })
})

app.get('/EmployeeRank/add',function(req, res)
{
    res.render('AddEmployeeRank')
}) 
app.post('/EmployeeRank/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/EmployeeRank/add', {
        RankTitle: req.body.RankTitle,
    })
    return res.redirect('/EmployeeRank')
})

app.get('/EmployeeRank/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/EmployeeRank/update/' + req.params.id)
    .then((response) => {
     var EmployeeRank = response.data;
    res.render('UpdateEmployeeRank',{
        EmployeeRank: EmployeeRank,
        id: req.params.id
    })
    })
})

app.post('/EmployeeRank/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/EmployeeRank/update/' + req.params.id, {
        RankTitle: req.body.RankTitle,
    })
    return res.redirect('/EmployeeRank')
})
app.get('/EmployeeRank/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/EmployeeRank/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/EmployeeRank')
})
//INCLUSION

app.get('/Inclusion/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Inclusion/') 
    .then((response) => {
     var Inclusion = response.data;
     console.log()
    res.render('Inclusion', {
        Inclusion: Inclusion
    })
    })
})
app.get('/Inclusion/add',function(req, res)
{
    res.render('AddInclusion')
})

app.post('/Inclusion/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Inclusion/add', {
        InclusionName: req.body.InclusionName,
    })
    return res.redirect('/Inclusion')
})

app.get('/Inclusion/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Inclusion/update/' + req.params.id)
    .then((response) => {
     var Inclusion = response.data;
    res.render('UpdateInclusion',{
        Inclusion: Inclusion,
        id: req.params.id
    })
    })
})

app.post('/Inclusion/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Inclusion/update/' + req.params.id, {
        InclusionName: req.body.InclusionName,
    })
    return res.redirect('/Inclusion')
})


app.get('/Inclusion/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Inclusion/delete/' + req.params.id)
    .then( function(response) {
        console.log(response.data);
    })
    return res.redirect('/Inclusion')
})

app.get('/Service/add',function(req, res)
{
    res.render('AddService')
})

app.get('/Service/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Service/') 
    .then((response) => {
     var Service = response.data;
     console.log(Service)
    res.render('Service', {
        Service: Service
    })
    })
})


app.post('/Service/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Service/add', { 
        ServiceName: req.body.ServiceName,
        TypeofService: req.body.TypeofService,
        ServicePrice: req.body.ServicePrice,
        ServiceDuration: req.body.ServiceDuration,
        ServiceDescription: req.body.ServiceDescription
    })
    return res.redirect('/Service')
})

/*
app.get('/Service/update/:id',function(req,res)
{
    res.render('UpdateService')
})
*/
app.get('/Service/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Service/update/' + req.params.id)
    .then((response) => {
     var Service = response.data;
    res.render('UpdateService',{
        Service: Service,
        id: req.params.id
    })
    })
})


app.post('/Service/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Service/update/' + req.params.id, {
        ServiceName: req.body.ServiceName,
        TypeofService: req.body.TypeofService,
        ServicePrice: req.body.ServicePrice,
        ServiceDuration: req.body.ServiceDuration,
        ServiceDescription: req.body.ServiceDescription

    })
    return res.redirect('/Service')
})

app.get('/Service/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Service/delete/' + req.params.id)
    .then(function(response) {
        console.log(response.data);
    })
    return res.redirect('/Service')
})

app.get('/Skill/add',function(req, res)
{
    res.render('AddSkill')
})

app.get('/Skill/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Skill/') 
    .then((response) => {
     var Skill = response.data;
     console.log(Skill)
    res.render('Skill', {
        Skill: Skill
    })
    })
})

app.post('/Skill/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Skill/add', { 
        SkillName: req.body.SkillName
    })
    return res.redirect('/Skill')
})

/*
app.get('/Skill/update/:id',function(req,res)
{
    res.render('UpdateSkill')
})
*/

app.get('/Skill/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Skill/update/' + req.params.id)
    
    .then((response) => {
     var Skill = response.data;
    res.render('UpdateSkill',{
        Skill: Skill,
        id: req.params.id
    })
    })

})

/* POST DOESNT WORK 
   FIXED! I have no idea why it works now but it does so thank God*/
app.post('/Skill/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Skill/update/' + req.params.id, {
        SkillName: req.body.SkillName
    })
    return res.redirect('/Skill')
})

app.get('/Skill/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Skill/delete/' + req.params.id)
    .then(function(response) {
        console.log(response.data);
    })
    return res.redirect('/Skill')
})

app.get('/Role/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/Role/') 
    .then((response) => {
     var Role = response.data;
     console.log(Role)
    res.render('Role', {
        Role: Role
    })
    })
})

app.get('/Role/add',function(req, res)
{
    res.render('AddRole')
})

app.post('/Role/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/Role/add', { 
        RoleTitle: req.body.RoleTitle,
        RoleDescription: req.body.RoleDescription
    })
    return res.redirect('/Role')
})

app.get('/Role/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/Role/update/' + req.params.id)
    
    .then((response) => {
     var Role = response.data;
    res.render('UpdateRole',{
        Role: Role,
        id: req.params.id
    })
    })
})

app.post('/Role/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/Role/update/' + req.params.id, {
        RoleTitle: req.body.RoleTitle,
        RoleDescription: req.body.RoleDescription
    })
    return res.redirect('/Role')
})

app.get('/Role/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/Role/delete/' + req.params.id)
    .then(function(response) {
        console.log(response.data);
    })
    return res.redirect('/Role')
})

app.get('/SatisfactionMeaning/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/SatisfactionMeaning/') 
    .then((response) => {
     var SatisfactionMeaning = response.data;
     console.log(SatisfactionMeaning)
    res.render('SatisfactionMeaning', {
        SatisfactionMeaning: SatisfactionMeaning
    })
    })
})

app.get('/SatisfactionMeaning/add',function(req, res)
{
    res.render('AddSatisfactionMeaning')
})

app.post('/SatisfactionMeaning/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/SatisfactionMeaning/add', { 
        AppointmentSatisfaction: req.body.AppointmentSatisfaction,
        SatisfactionMeaning: req.body.SatisfactionMeaning
    })
    return res.redirect('/SatisfactionMeaning')
})

app.get('/SatisfactionMeaning/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/SatisfactionMeaning/update/' + req.params.id)
    
    .then((response) => {
     var SatisfactionMeaning = response.data;
    res.render('UpdateSatisfactionMeaning',{
        SatisfactionMeaning: SatisfactionMeaning,
        id: req.params.id
    })
    })
})

app.post('/SatisfactionMeaning/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/SatisfactionMeaning/update/' + req.params.id, {
        AppointmentSatisfaction: req.body.AppointmentSatisfaction,
        SatisfactionMeaning: req.body.SatisfactionMeaning
    })
    return res.redirect('/SatisfactionMeaning')
})

app.get('/SatisfactionMeaning/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/SatisfactionMeaning/delete/' + req.params.id)
    .then(function(response) {
        console.log(response.data);
    })
    return res.redirect('/SatisfactionMeaning')
})

app.get('/ProductType/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/ProductType/') 
    .then((response) => {
     var ProductType = response.data;
     console.log(ProductType)
    res.render('ProductType', {
        ProductType: ProductType
    })
    })
})

app.get('/ProductType/add',function(req, res)
{
    res.render('AddProductType')
})

app.post('/ProductType/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/ProductType/add', { 
        ProductType: req.body.ProductType,
        Color: req.body.Color
    })
    return res.redirect('/ProductType')
})

app.get('/ProductType/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/ProductType/update/' + req.params.id)
    
    .then((response) => {
     var ProductType = response.data;
    res.render('UpdateProductType',{
        ProductType: ProductType,
        id: req.params.id
    })
    })
})

app.post('/ProductType/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/ProductType/update/' + req.params.id, {
        ProductType: req.body.ProductType,
        Color: req.body.Color
    })
    return res.redirect('/ProductType')
})

app.get('/ProductType/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/ProductType/delete/' + req.params.id)
    .then(function(response) {
        console.log(response.data);
    })
    return res.redirect('/ProductType')
})

app.get('/HairProduct/',function(req, res)
{
    axios.get('http://127.0.0.1:5000/HairProduct/') 
    .then((response) => {
     var HairProduct = response.data;
     console.log(HairProduct)
    res.render('HairProduct', {
        HairProduct: HairProduct
    })
    })
})

app.get('/HairProduct/add',function(req, res)
{
    res.render('AddHairProduct')
})

app.post('/HairProduct/add',function(req, res)
{
    axios.post('http://127.0.0.1:5000/HairProduct/add', { 
        ProductType: req.body.ProductType,
        Color: req.body.Color,
        ProductName: req.body.ProductName,
        ProductDescription: req.body.ProductDescription,
        ProductVolume: req.body.ProductVolume
    })
    return res.redirect('/HairProduct')
})

app.get('/HairProduct/update/:id',function(req,res)
{
    axios.get('http://127.0.0.1:5000/HairProduct/update/' + req.params.id)
    .then((response) => {
     var HairProduct = response.data
     var ProductType = response.data;
    res.render('UpdateHairProduct',{
        HairProduct: HairProduct,
        ProductType: ProductType,
        id: req.params.id
    })
    })
})


app.post('/HairProduct/update/:id',function(req,res)
{
    axios.put('http://127.0.0.1:5000/HairProduct/update/' + req.params.id, {
        ProductType: req.body.ProductType,
        Color: req.body.Color,
        ProductName: req.body.ProductName,
        ProductDescription: req.body.ProductDescription,
        ProductVolume: req.body.ProductVolume

    })
    return res.redirect('/HairProduct')
})

app.get('/HairProduct/delete/:id',function(req,res)
{
    axios.delete('http://127.0.0.1:5000/HairProduct/delete/' + req.params.id)
    .then(function(response) {
        console.log(response.data);
    })
    return res.redirect('/HairProduct')
})

//Start the express application on port 8080 and print server start message to console.
app.listen(port, () => {
    console.log(`Front-end app listening at http://localhost:${port}/`)
});