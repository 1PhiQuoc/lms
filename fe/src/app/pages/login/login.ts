import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { toggleAnimation } from '../../shared/animations';
import { Store } from '@ngrx/store';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';

@Component({
    selector: 'app-login',
    standalone: true,
    templateUrl: './login.html',
    styleUrls: ['./login.scss'],
    animations: [toggleAnimation],
    imports: [CommonModule, RouterModule, ReactiveFormsModule],
})
export class Login {
    store: any;
    form: FormGroup;
    data: {
        username: string;
        password: string;
    } = {
        username: '',
        password: '',
    }

    constructor(private fb: FormBuilder) {
        this.form = this.fb.group({
            username: ['', Validators.required],
            password: ['', Validators.required],
        });
    }

    onSubmit() {
        console.log('Form submitted:', this.data.username, this.data.password);
        if (this.form.valid) {
            console.log('Form submitted:', this.form.value);
            // TODO: call API or navigate
        } else {
            console.log('Form invalid');
        }
    }
}
